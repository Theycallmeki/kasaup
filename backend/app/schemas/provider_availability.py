from pydantic import BaseModel, field_validator
from datetime import time, datetime


def parse_time_12h(value):
    if isinstance(value, time):
        return value
    return datetime.strptime(value, "%I:%M %p").time()


class ProviderAvailabilityCreate(BaseModel):
    provider_id: int
    day_of_week: int
    start_time: time
    end_time: time

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def convert_time(cls, v):
        return parse_time_12h(v)


class ProviderAvailabilityUpdate(BaseModel):
    day_of_week: int | None = None
    start_time: time | None = None
    end_time: time | None = None

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def convert_time(cls, v):
        if v is None:
            return v
        return parse_time_12h(v)


class ProviderAvailabilityResponse(BaseModel):
    id: int
    provider_id: int
    day_of_week: int
    start_time: time
    end_time: time

    class Config:
        from_attributes = True