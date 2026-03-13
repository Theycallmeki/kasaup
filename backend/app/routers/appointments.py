from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.appointment import Appointment
from app.models.providers import Provider
from app.models.users import User
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
)
from app.core.dependencies import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider = db.query(Provider).filter(Provider.id == appointment.provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    new_appointment = Appointment(
        user_id=current_user.id,
        provider_id=appointment.provider_id,
        appointment_time=appointment.appointment_time,
        status=appointment.status
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


@router.get("/", response_model=list[AppointmentResponse])
def get_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "provider":
        providers = db.query(Provider).filter(Provider.owner_id == current_user.id).all()
        provider_ids = [p.id for p in providers]
        return db.query(Appointment).filter(Appointment.provider_id.in_(provider_ids)).all()

    return db.query(Appointment).filter(Appointment.user_id == current_user.id).all()


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if current_user.role == "customer" and appointment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if current_user.role == "provider":
        provider = db.query(Provider).filter(Provider.id == appointment.provider_id).first()
        if provider.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")

    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    provider = db.query(Provider).filter(Provider.id == db_appointment.provider_id).first()

    if current_user.role == "provider" and provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if current_user.role == "customer" and db_appointment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for key, value in appointment.dict(exclude_unset=True).items():
        setattr(db_appointment, key, value)

    db.commit()
    db.refresh(db_appointment)

    return db_appointment


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    provider = db.query(Provider).filter(Provider.id == appointment.provider_id).first()

    if current_user.role == "provider" and provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if current_user.role == "customer" and appointment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(appointment)
    db.commit()

    return {"message": "Appointment deleted"}