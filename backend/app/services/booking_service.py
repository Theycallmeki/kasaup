from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.appointment import Appointment
from app.models.provider_availability import ProviderAvailability


def create_booking(
    db: Session,
    user_id: int,
    provider_id: int,
    service_id: int,
    appointment_time: datetime,
    duration_minutes: int,
    customer_latitude: float | None = None,
    customer_longitude: float | None = None,
):
    end_time = appointment_time + timedelta(minutes=duration_minutes)

    existing = db.query(Appointment).filter(
        Appointment.provider_id == provider_id
    ).all()

    for booking in existing:
        if booking.status in ("cancelled", "completed"):
            continue

        booking_end = booking.appointment_time + timedelta(minutes=booking.duration_minutes)

        if (
            appointment_time < booking_end and
            end_time > booking.appointment_time
        ):
            raise ValueError("Time slot overlaps with another appointment")

    weekday = (appointment_time.weekday() + 1) % 7

    availability = db.query(ProviderAvailability).filter(
        ProviderAvailability.provider_id == provider_id,
        ProviderAvailability.day_of_week == weekday
    ).all()

    if not availability:
        raise ValueError("Provider not available on this day")

    valid_slot = False

    for avail in availability:
        avail_start = datetime.combine(appointment_time.date(), avail.start_time)
        avail_end = datetime.combine(appointment_time.date(), avail.end_time)

        if appointment_time >= avail_start and end_time <= avail_end:
            valid_slot = True
            break

    if not valid_slot:
        raise ValueError("Appointment time outside provider availability")

    new_booking = Appointment(
        user_id=user_id,
        provider_id=provider_id,
        service_id=service_id,
        appointment_time=appointment_time,
        duration_minutes=duration_minutes,
        status="pending",
        customer_latitude=customer_latitude,
        customer_longitude=customer_longitude
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


def update_status(
    db: Session,
    appointment: Appointment,
    new_status: str
):
    allowed_transitions = {
        "pending": ["approved", "cancelled"],
        "approved": ["completed", "cancelled"],
        "confirmed": ["completed", "cancelled"],
        "completed": [],
        "cancelled": [],
    }

    current_status = appointment.status

    if new_status not in allowed_transitions[current_status]:
        raise ValueError(
            f"Cannot change status from {current_status} to {new_status}"
        )

    appointment.status = new_status

    if new_status == "completed":
        appointment.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(appointment)

    return appointment