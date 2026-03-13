from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.provider_availability import ProviderAvailability
from app.models.providers import Provider
from app.models.users import User
from app.schemas.provider_availability import (
    ProviderAvailabilityCreate,
    ProviderAvailabilityUpdate,
    ProviderAvailabilityResponse,
)
from app.core.dependencies import require_provider

router = APIRouter(dependencies=[Depends(require_provider)])


@router.post("/", response_model=ProviderAvailabilityResponse)
def create_availability(
    availability: ProviderAvailabilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    provider = db.query(Provider).filter(Provider.id == availability.provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    if provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    new_availability = ProviderAvailability(**availability.dict())

    db.add(new_availability)
    db.commit()
    db.refresh(new_availability)

    return new_availability


@router.get("/{provider_id}", response_model=list[ProviderAvailabilityResponse])
def get_availability(
    provider_id: int,
    db: Session = Depends(get_db)
):
    availability = db.query(ProviderAvailability).filter(
        ProviderAvailability.provider_id == provider_id
    ).all()

    return availability


@router.put("/{availability_id}", response_model=ProviderAvailabilityResponse)
def update_availability(
    availability_id: int,
    availability: ProviderAvailabilityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    db_availability = db.query(ProviderAvailability).filter(
        ProviderAvailability.id == availability_id
    ).first()

    if not db_availability:
        raise HTTPException(status_code=404, detail="Availability not found")

    provider = db.query(Provider).filter(
        Provider.id == db_availability.provider_id
    ).first()

    if provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for key, value in availability.dict(exclude_unset=True).items():
        setattr(db_availability, key, value)

    db.commit()
    db.refresh(db_availability)

    return db_availability


@router.delete("/{availability_id}")
def delete_availability(
    availability_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    db_availability = db.query(ProviderAvailability).filter(
        ProviderAvailability.id == availability_id
    ).first()

    if not db_availability:
        raise HTTPException(status_code=404, detail="Availability not found")

    provider = db.query(Provider).filter(
        Provider.id == db_availability.provider_id
    ).first()

    if provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(db_availability)
    db.commit()

    return {"message": "Availability deleted"}