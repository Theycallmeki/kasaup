from pydantic import BaseModel, Field
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
    images: List[str] = Field(default_factory=list)


class ServiceUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    duration_minutes: int | None = None


class ServiceResponse(BaseModel):
    id: int
    provider_id: int
    category_id: int
    name: str
    description: str | None
    price: float
    duration_minutes: int
    images: List[ServiceImage] = Field(default_factory=list)

    class Config:
        from_attributes = True