from pydantic import BaseModel
from datetime import time


class ProviderAvailabilityCreate(BaseModel):
    provider_id: int
    day_of_week: int
    start_time: time
    end_time: time


class ProviderAvailabilityUpdate(BaseModel):
    day_of_week: int | None = None
    start_time: time | None = None
    end_time: time | None = None


class ProviderAvailabilityResponse(BaseModel):
    id: int
    provider_id: int
    day_of_week: int
    start_time: time
    end_time: time

    class Config:
        from_attributes = True