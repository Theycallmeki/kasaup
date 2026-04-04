from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db import get_db
from app.models.appointment import Appointment
from app.models.providers import Provider
from app.models.provider_availability import ProviderAvailability
from app.models.service import Service
from app.models.users import User
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
)
from app.core.dependencies import get_current_user
from app.services.booking_service import create_booking, update_status

router = APIRouter()


@router.post("/", response_model=AppointmentResponse, dependencies=[Depends(get_current_user)])
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = db.query(Provider).filter(Provider.id == appointment.provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    service = db.query(Service).filter(Service.id == appointment.service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    try:
        booking = create_booking(
            db=db,
            user_id=current_user.id,
            provider_id=appointment.provider_id,
            service_id=appointment.service_id,
            appointment_time=appointment.appointment_time,
            duration_minutes=service.duration_minutes,
            customer_latitude=appointment.customer_latitude,
            customer_longitude=appointment.customer_longitude,
        )
        return {
            **booking.__dict__,
            "service_name": booking.service.name,
            "customer_name": booking.user.full_name,
            "provider_name": booking.provider.shop_name,
            "user_rating": booking.review.rating if booking.review else None,
            "customer_profile_image": booking.user.profile_image
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[AppointmentResponse], dependencies=[Depends(get_current_user)])
def get_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "provider":
        providers = db.query(Provider).filter(
            Provider.owner_id == current_user.id
        ).all()

        provider_ids = [p.id for p in providers]

        appointments = db.query(Appointment).filter(
            Appointment.provider_id.in_(provider_ids)
        ).order_by(Appointment.id.desc()).all()
    else:
        appointments = db.query(Appointment).filter(
            Appointment.user_id == current_user.id
        ).order_by(Appointment.id.desc()).all()

    return [
        {
            **a.__dict__,
            "service_name": a.service.name,
            "customer_name": a.user.full_name,
            "provider_name": a.provider.shop_name,
            "user_rating": a.review.rating if getattr(a, "review", None) else None,
            "customer_profile_image": a.user.profile_image
        }
        for a in appointments
    ]


@router.put("/{appointment_id}/approve/")
def approve_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(404, "Appointment not found")

    provider = db.query(Provider).filter(
        Provider.id == appointment.provider_id
    ).first()

    if current_user.role != "provider" or provider.owner_id != current_user.id:
        raise HTTPException(403, "Not authorized")

    try:
        return update_status(db, appointment, "approved")
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.put("/{appointment_id}/cancel/")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(404, "Appointment not found")

    provider = db.query(Provider).filter(
        Provider.id == appointment.provider_id
    ).first()

    is_customer = appointment.user_id == current_user.id
    is_provider = (
        current_user.role == "provider" and
        provider.owner_id == current_user.id
    )

    if not (is_customer or is_provider):
        raise HTTPException(403, "Not authorized")

    try:
        return update_status(db, appointment, "cancelled")
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.put("/{appointment_id}/complete/")
def complete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(404, "Appointment not found")

    provider = db.query(Provider).filter(
        Provider.id == appointment.provider_id
    ).first()

    if current_user.role != "provider" or provider.owner_id != current_user.id:
        raise HTTPException(403, "Not authorized")

    try:
        return update_status(db, appointment, "completed")
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/providers/{provider_id}/available-slots/")
def get_available_slots(
    provider_id: int,
    db: Session = Depends(get_db)
):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    start = datetime.now().replace(minute=0, second=0, microsecond=0)
    end = start + timedelta(days=7)

    availability = db.query(ProviderAvailability).filter(
        ProviderAvailability.provider_id == provider_id
    ).all()

    if not availability:
        return {"available_slots": []}

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.provider_id == provider_id,
            Appointment.appointment_time >= start,
            Appointment.appointment_time <= end,
            Appointment.status.in_(["pending", "approved", "confirmed"]),
        )
        .all()
    )

    booked_times = {a.appointment_time for a in appointments}

    slots = []
    current = start

    while current <= end:
        weekday = (current.weekday() + 1) % 7

        day_availability = [
            a for a in availability if a.day_of_week == weekday
        ]

        for avail in day_availability:
            slot_time = current.replace(
                hour=avail.start_time.hour,
                minute=avail.start_time.minute
            )

            if slot_time not in booked_times and slot_time >= start:
                slots.append(slot_time)

        current += timedelta(days=1)

    return {"available_slots": slots}


@router.get("/services/{service_id}/available-slots/")
def get_service_available_slots(
    service_id: int,
    date: str,
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    provider = db.query(Provider).filter(Provider.id == service.provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d")
    except:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    weekday = (selected_date.weekday() + 1) % 7

    availability = db.query(ProviderAvailability).filter(
        ProviderAvailability.provider_id == provider.id,
        ProviderAvailability.day_of_week == weekday
    ).all()

    if not availability:
        return {"available_slots": []}

    day_start = selected_date.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = selected_date.replace(hour=23, minute=59, second=59, microsecond=0)

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.provider_id == provider.id,
            Appointment.appointment_time >= day_start,
            Appointment.appointment_time <= day_end,
            Appointment.status.in_(["pending", "approved", "confirmed"]),
        )
        .all()
    )

    slots = []

    for avail in availability:
        slot_time = selected_date.replace(
            hour=avail.start_time.hour,
            minute=avail.start_time.minute,
            second=0,
            microsecond=0
        )

        end_time = selected_date.replace(
            hour=avail.end_time.hour,
            minute=avail.end_time.minute,
            second=0,
            microsecond=0
        )

        overlap = False
        for appt in appointments:
            appt_start = appt.appointment_time
            appt_end = appt_start + timedelta(minutes=appt.service.duration_minutes)

            if not (end_time <= appt_start or slot_time >= appt_end):
                overlap = True
                break

        if not overlap and slot_time >= datetime.now():
            slots.append({
                "start_time": slot_time,
                "end_time": end_time
            })

    return {"available_slots": slots}


@router.get("/{appointment_id}/", response_model=AppointmentResponse, dependencies=[Depends(get_current_user)])
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if current_user.role == "customer" and appointment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if current_user.role == "provider":
        provider = db.query(Provider).filter(
            Provider.id == appointment.provider_id
        ).first()

        if provider.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")

    return {
        **appointment.__dict__,
        "service_name": appointment.service.name,
        "customer_name": appointment.user.full_name,
        "provider_name": appointment.provider.shop_name,
        "user_rating": appointment.review.rating if getattr(appointment, "review", None) else None
    }


@router.put("/{appointment_id}/", response_model=AppointmentResponse, dependencies=[Depends(get_current_user)])
def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    provider = db.query(Provider).filter(
        Provider.id == db_appointment.provider_id
    ).first()

    if current_user.role == "provider" and provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if current_user.role == "customer" and db_appointment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = appointment.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_appointment, key, value)

    db.commit()
    db.refresh(db_appointment)

    return {
        **db_appointment.__dict__,
        "service_name": db_appointment.service.name,
        "customer_name": db_appointment.user.full_name,
        "provider_name": db_appointment.provider.shop_name,
        "user_rating": db_appointment.review.rating if getattr(db_appointment, "review", None) else None
    }


@router.delete("/{appointment_id}/", dependencies=[Depends(get_current_user)])
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    provider = db.query(Provider).filter(
        Provider.id == appointment.provider_id
    ).first()

    if current_user.role == "provider" and provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if current_user.role == "customer" and appointment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(appointment)
    db.commit()

    return {"message": "Appointment deleted"}