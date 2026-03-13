from pydantic import BaseModel
from datetime import datetime


class ProviderCreate(BaseModel):
    shop_name: str
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    latitude: float
    longitude: float
    offers_home_service: bool


class ProviderUpdate(BaseModel):
    shop_name: str
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    latitude: float
    longitude: float
    offers_home_service: bool


class ProviderResponse(BaseModel):
    id: int
    owner_id: int
    shop_name: str
    description: str | None
    phone: str | None
    email: str | None
    address: str | None
    latitude: float
    longitude: float
    offers_home_service: bool
    rating: float
    total_reviews: int
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True