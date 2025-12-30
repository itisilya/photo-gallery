import uuid
from datetime import datetime
from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.concurrency import run_in_threadpool  # Для синхронного S3
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

from .database import photos_collection
from .models import PhotoResponse, PhotoUpdate
from .storage import storage

app = FastAPI(title="Yandex Cloud Photo Gallery")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    print("Приложение запускается...")


@app.post("/api/photos/upload", response_model=PhotoResponse)
async def upload_photo(
        title: str = Form(...),
        description: str = Form(None),
        file: UploadFile = File(...)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG/PNG allowed")

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    # Чтобы синхронный boto3 не вешал сервер, запускаем его в отдельном потоке
    try:
        file_url = await run_in_threadpool(storage.save, file.file, filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 Upload Error: {str(e)}")

    new_photo = {
        "title": title,
        "description": description,
        "filename": filename,
        "url": file_url,
        "upload_date": datetime.utcnow()
    }

    result = await photos_collection.insert_one(new_photo)

    response_data = {
        "id": str(result.inserted_id),  # Явно приводим к строке
        "title": title,
        "description": description,
        "filename": filename,
        "url": file_url,
        "upload_date": new_photo["upload_date"]
    }

    return response_data


@app.get("/api/photos", response_model=List[PhotoResponse])
async def list_photos():
    photos = []
    # Мы берем данные из БД, так как только там есть Title и Description
    async for photo in photos_collection.find():
        photos.append({
            "id": str(photo["_id"]),
            "title": photo["title"],
            "description": photo.get("description"),
            "filename": photo["filename"],
            "url": photo.get("url"),  # Это уже ссылка на Yandex Cloud S3
            "upload_date": photo["upload_date"]
        })
    return photos


@app.get("/api/photos/{photo_id}", response_model=PhotoResponse)
async def get_photo(photo_id: str):
    # Проверяем, что ID валидный для MongoDB
    if not ObjectId.is_valid(photo_id):
        raise HTTPException(status_code=400, detail="Неверный формат ID")

    # Ищем в базе
    photo = await photos_collection.find_one({"_id": ObjectId(photo_id)})

    if not photo:
        raise HTTPException(status_code=404, detail="Фото не найдено")

    return {
        "id": str(photo["_id"]),
        "title": photo["title"],
        "description": photo.get("description"),
        "filename": photo["filename"],
        "url": photo.get("url"),
        "upload_date": photo["upload_date"]
    }


@app.patch("/api/photos/{photo_id}")
async def update_photo(photo_id: str, update_data: PhotoUpdate):
    if not ObjectId.is_valid(photo_id):
        raise HTTPException(status_code=400, detail="Неверный формат ID")

    # Формируем словарь только из тех полей, которые были присланы
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}

    if not update_dict:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")

    # Обновляем в MongoDB
    result = await photos_collection.update_one(
        {"_id": ObjectId(photo_id)},
        {"$set": update_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Фото не найдено")

    return {"status": "success", "updated_fields": list(update_dict.keys())}

@app.delete("/api/photos/{photo_id}")
async def delete_photo(photo_id: str):
    if not ObjectId.is_valid(photo_id):
        raise HTTPException(status_code=400, detail="Неверный формат ID")

    # 1. Ищем информацию о фото в базе, чтобы узнать имя файла (filename)
    photo = await photos_collection.find_one({"_id": ObjectId(photo_id)})
    if not photo:
        raise HTTPException(status_code=404, detail="Фото не найдено в базе данных")

    filename = photo.get("filename")

    # 2. Удаляем файл из Yandex Object Storage
    if filename:
        try:
            # Выполняем синхронное удаление в отдельном потоке
            await run_in_threadpool(storage.delete, filename)
        except Exception as e:
            print(f"Предупреждение: не удалось удалить файл из S3: {e}")

    # 3. Удаляем запись из MongoDB
    await photos_collection.delete_one({"_id": ObjectId(photo_id)})

    return {"status": "success", "message": f"Фото {photo_id} и файл {filename} удалены"}