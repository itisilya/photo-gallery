from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

# Вспомогательный класс для работы с ObjectId из MongoDB
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class PhotoBase(BaseModel):
    title: str
    description: Optional[str] = None

class PhotoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class PhotoCreate(PhotoBase):
    pass

class PhotoResponse(BaseModel):
    # Это позволит Pydantic правильно обрабатывать данные из словарей MongoDB
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="ID документа в формате строки")
    title: str
    description: Optional[str] = None
    filename: str
    url: str
    thumb_url: Optional[str] = None
    upload_date: datetime