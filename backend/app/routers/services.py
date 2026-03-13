from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.service import Service
from app.models.providers import Provider
from app.models.users import User
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.core.dependencies import require_provider

router = APIRouter(dependencies=[Depends(require_provider)])


@router.post("/", response_model=ServiceResponse)
def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    provider = db.query(Provider).filter(Provider.id == service.provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    if provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    new_service = Service(**service.dict())

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


@router.get("/", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service


@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    service: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    db_service = db.query(Service).filter(Service.id == service_id).first()

    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    provider = db.query(Provider).filter(Provider.id == db_service.provider_id).first()

    if provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for key, value in service.dict().items():
        setattr(db_service, key, value)

    db.commit()
    db.refresh(db_service)

    return db_service


@router.delete("/{service_id}")
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    provider = db.query(Provider).filter(Provider.id == service.provider_id).first()

    if provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(service)
    db.commit()

    return {"message": "Service deleted"}