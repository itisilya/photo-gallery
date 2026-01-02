import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Загружаем переменные окружения строго перед инициализацией
load_dotenv()


class S3Storage:
    def __init__(self):
        print("--- Инициализация S3 клиента... ---")
        self.bucket_name = os.getenv("S3_BUCKET_NAME")

        # Проверка наличия ключей (чтобы не гадать)
        if not all([os.getenv("S3_ACCESS_KEY"), os.getenv("S3_SECRET_KEY")]):
            print("ОШИБКА: Ключи доступа S3 не найдены в .env!")

        try:
            self.session = boto3.session.Session()
            self.s3 = self.session.client(
                service_name='s3',
                endpoint_url=os.getenv("S3_ENDPOINT"),
                aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
                aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
                region_name=os.getenv("S3_REGION")
            )
            print(f"--- S3 клиент готов (Бакет: {self.bucket_name}) ---")
        except Exception as e:
            print(f"ОШИБКА инициализации S3: {e}")

    def save(self, file, filename: str) -> str:
        try:
            print(f"Загрузка файла {filename} в S3...")
            self.s3.upload_fileobj(
                file,
                self.bucket_name,
                filename,
                ExtraArgs={'ACL': 'public-read'}
            )
            url = f"{os.getenv('S3_ENDPOINT')}/{self.bucket_name}/{filename}"
            print(f"Файл успешно загружен: {url}")
            return url
        except Exception as e:
            print(f"Ошибка при загрузке в S3: {e}")
            raise

    def delete(self, filename: str):
        try:
            # Формируем список объектов для удаления
            objects_to_delete = [
                {'Key': filename},  # Оригинал
                {'Key': f"thumb_{filename}"}  # Превью
            ]

            print(f"Попытка удаления файлов: {filename} и thumb_{filename}...")

            # Удаляем несколько объектов сразу
            response = self.s3.delete_objects(
                Bucket=self.bucket_name,
                Delete={
                    'Objects': objects_to_delete,
                    'Quiet': True  # Не возвращать детали по каждому файлу, если всё ок
                }
            )
            print(f"Удаление из S3 завершено успешно.")

        except Exception as e:
            print(f"Ошибка при удалении из S3: {e}")


# Создаем объект
storage = S3Storage()