from pydantic import BaseModel
from typing import List


class ServiceImage(BaseModel):
    id: int
    image_url: str

    class Config:
        from_attributes = True


class ServiceCreate(BaseModel):
    category_id: int
    name: str
    description: str | None = None
    price: float
    duration_minutes: int
    images: List[str] = []


class ServiceUpdate(BaseModel):
    category_id: int
    name: str
    description: str | None = None
    price: float
    duration_minutes: int


class ServiceResponse(BaseModel):
    id: int
    provider_id: int
    category_id: int
    name: str
    description: str | None
    price: float
    duration_minutes: int
    images: List[ServiceImage] = []

    class Config:
        from_attributes = True