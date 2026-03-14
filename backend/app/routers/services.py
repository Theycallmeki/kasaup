from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.service import Service
from app.models.providers import Provider
from app.models.users import User
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.core.dependencies import require_provider
from app.services.service_search_service import search_services

router = APIRouter()


@router.post("/", response_model=ServiceResponse, dependencies=[Depends(require_provider)])
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
def get_services(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return db.query(Service).offset(offset).limit(limit).all()


@router.get("/search")
def search(
    q: str | None = None,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db)
):
    return search_services(
        db,
        query=q,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price
    )


@router.get("/provider/{provider_id}", response_model=list[ServiceResponse])
def get_services_by_provider(
    provider_id: int,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    services = db.query(Service).filter(
        Service.provider_id == provider_id
    ).offset(offset).limit(limit).all()

    return services


@router.get("/category/{category_id}", response_model=list[ServiceResponse])
def get_services_by_category(
    category_id: int,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    services = db.query(Service).filter(
        Service.category_id == category_id
    ).offset(offset).limit(limit).all()

    return services


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service


@router.put("/{service_id}", response_model=ServiceResponse, dependencies=[Depends(require_provider)])
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

    update_data = service.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_service, key, value)

    db.commit()
    db.refresh(db_service)

    return db_service


@router.delete("/{service_id}", dependencies=[Depends(require_provider)])
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