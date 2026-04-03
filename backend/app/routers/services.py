from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.service import Service
from app.models.providers import Provider
from app.models.users import User
from app.models.service_image import ServiceImage
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.core.dependencies import require_provider
from app.services.service_search_service import search_services
from app.services.upload_service import save_multiple_images

router = APIRouter()


@router.post("/", response_model=ServiceResponse)
def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    provider = db.query(Provider).filter(
        Provider.owner_id == current_user.id
    ).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    new_service = Service(
        provider_id=provider.id,
        category_id=service.category_id,
        name=service.name,
        description=service.description,
        price=service.price,
        duration_minutes=service.duration_minutes
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    if service.images:
        for img in service.images:
            db.add(ServiceImage(service_id=new_service.id, image_url=img))
        db.commit()

    db.refresh(new_service)
    return new_service


@router.post("/{service_id}/images/")
def upload_service_images(
    service_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    provider = db.query(Provider).filter(
        Provider.id == service.provider_id
    ).first()

    if provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    paths = save_multiple_images(files)

    for path in paths:
        db.add(ServiceImage(service_id=service.id, image_url=path))

    db.commit()

    return {"images": paths}


@router.get("/", response_model=list[ServiceResponse])
def get_services(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return db.query(Service).offset(offset).limit(limit).all()


@router.get("/search/", response_model=list[ServiceResponse])
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


@router.get("/provider/{provider_id}/", response_model=list[ServiceResponse])
def get_services_by_provider(
    provider_id: int,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return db.query(Service).filter(
        Service.provider_id == provider_id
    ).offset(offset).limit(limit).all()


@router.get("/category/{category_id}/", response_model=list[ServiceResponse])
def get_services_by_category(
    category_id: int,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return db.query(Service).filter(
        Service.category_id == category_id
    ).offset(offset).limit(limit).all()


@router.get("/{service_id}/", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service


@router.put("/{service_id}/", response_model=ServiceResponse)
def update_service(
    service_id: int,
    service: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    db_service = db.query(Service).filter(Service.id == service_id).first()

    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    provider = db.query(Provider).filter(
        Provider.id == db_service.provider_id
    ).first()

    if provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = service.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_service, key, value)

    db.commit()
    db.refresh(db_service)

    return db_service


@router.delete("/{service_id}/")
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    provider = db.query(Provider).filter(
        Provider.id == service.provider_id
    ).first()

    if provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(service)
    db.commit()

    return {"message": "Service deleted"}


@router.delete("/{service_id}/images/{image_id}/")
def delete_service_image(
    service_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    image = db.query(ServiceImage).filter(
        ServiceImage.id == image_id,
        ServiceImage.service_id == service_id
    ).first()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    service = db.query(Service).filter(Service.id == service_id).first()

    provider = db.query(Provider).filter(
        Provider.id == service.provider_id
    ).first()

    if provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(image)
    db.commit()

    return {"message": "Image deleted"}