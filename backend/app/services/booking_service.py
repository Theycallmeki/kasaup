from sqlalchemy.orm import Session
from datetime import datetime

from app.models.appointment import Appointment
from app.models.provider_availability import ProviderAvailability


def create_booking(
    db: Session,
    user_id: int,
    provider_id: int,
    appointment_time: datetime,
    status: str = "pending"
):
    existing = (
        db.query(Appointment)
        .filter(
            Appointment.provider_id == provider_id,
            Appointment.appointment_time == appointment_time
        )
        .first()
    )

    if existing:
        raise ValueError("Time slot already booked")

    weekday = appointment_time.weekday()

    availability = db.query(ProviderAvailability).filter(
        ProviderAvailability.provider_id == provider_id,
        ProviderAvailability.day_of_week == weekday
    ).all()

    if not availability:
        raise ValueError("Provider not available on this day")

    valid_slot = False

    for avail in availability:
        if avail.start_time <= appointment_time.time() < avail.end_time:
            valid_slot = True
            break

    if not valid_slot:
        raise ValueError("Appointment time outside provider availability")

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