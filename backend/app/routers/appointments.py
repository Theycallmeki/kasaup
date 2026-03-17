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
        return booking

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[AppointmentResponse], dependencies=[Depends(get_current_user)])
def get_appointments(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "provider":
        providers = db.query(Provider).filter(Provider.owner_id == current_user.id).all()
        provider_ids = [p.id for p in providers]

        return db.query(Appointment).filter(
            Appointment.provider_id.in_(provider_ids)
        ).offset(offset).limit(limit).all()

    return db.query(Appointment).filter(
        Appointment.user_id == current_user.id
    ).offset(offset).limit(limit).all()


@router.put("/{appointment_id}/confirm")
def confirm_appointment(
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
        return update_status(db, appointment, "confirmed")
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.put("/{appointment_id}/cancel")
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


@router.put("/{appointment_id}/complete")
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


@router.get("/providers/{provider_id}/available-slots")
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
            Appointment.appointment_time <= end
        )
        .all()
    )

    booked_times = {a.appointment_time for a in appointments}

    slots = []
    current = start

    while current <= end:
        weekday = current.weekday()

        day_availability = [
            a for a in availability if a.day_of_week == weekday
        ]

        for avail in day_availability:
            slot_time = current.replace(
                hour=avail.start_time.hour,
                minute=avail.start_time.minute
            )

            while slot_time.time() < avail.end_time:
                if slot_time not in booked_times and slot_time >= start:
                    slots.append(slot_time)

                slot_time += timedelta(hours=1)

        current += timedelta(days=1)

    return {"available_slots": slots}


@router.get("/services/{service_id}/available-slots")
def get_service_available_slots(
    service_id: int,
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    provider = db.query(Provider).filter(Provider.id == service.provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    start = datetime.now().replace(minute=0, second=0, microsecond=0)
    end = start + timedelta(days=7)

    availability = db.query(ProviderAvailability).filter(
        ProviderAvailability.provider_id == provider.id
    ).all()

    if not availability:
        return {"available_slots": []}

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.provider_id == provider.id,
            Appointment.appointment_time >= start,
            Appointment.appointment_time <= end
        )
        .all()
    )

    booked_times = {a.appointment_time for a in appointments}

    slots = []
    current = start

    while current <= end:
        weekday = current.weekday()

        day_availability = [
            a for a in availability if a.day_of_week == weekday
        ]

        for avail in day_availability:
            slot_time = current.replace(
                hour=avail.start_time.hour,
                minute=avail.start_time.minute
            )

            while slot_time.time() < avail.end_time:
                if slot_time not in booked_times and slot_time >= start:
                    slots.append(slot_time)

                slot_time += timedelta(minutes=service.duration_minutes)

        current += timedelta(days=1)

    return {"available_slots": slots}


@router.get("/{appointment_id}", response_model=AppointmentResponse, dependencies=[Depends(get_current_user)])
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

    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse, dependencies=[Depends(get_current_user)])
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

    return db_appointment


@router.delete("/{appointment_id}", dependencies=[Depends(get_current_user)])
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