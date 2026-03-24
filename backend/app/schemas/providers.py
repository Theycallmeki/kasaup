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
    owner_id: int | None = None
    shop_name: str
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    latitude: float
    longitude: float
    offers_home_service: bool
    profile_image: str | None = None
    rating: float | None = None
    total_reviews: int | None = None
    is_verified: bool | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class ProviderListItem(ProviderResponse):
    service_names: list[str] = []
    category_names: list[str] = []