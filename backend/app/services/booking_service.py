from sqlalchemy.orm import Session
from datetime import datetime

from app.models.appointment import Appointment


def create_booking(
    db: Session,
    user_id: int,
    provider_id: int,
    appointment_time: datetime,
    status: str = "pending"
):
    new_booking = Appointment(
        user_id=user_id,
        provider_id=provider_id,
        appointment_time=appointment_time,
        status=status
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking