from pydantic import BaseModel


class ServiceCreate(BaseModel):
    provider_id: int
    category_id: int
    name: str
    description: str | None = None
    price: float
    duration_minutes: int
    latitude: float | None = None
    longitude: float | None = None


class ServiceUpdate(BaseModel):
    category_id: int
    name: str
    description: str | None = None
    price: float
    duration_minutes: int
    latitude: float | None = None
    longitude: float | None = None


class ServiceResponse(BaseModel):
    id: int
    provider_id: int
    category_id: int
    name: str
    description: str | None
    price: float
    duration_minutes: int
    latitude: float | None
    longitude: float | None

    class Config:
        from_attributes = True