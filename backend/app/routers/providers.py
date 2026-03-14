from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.providers import Provider
from app.models.service import Service
from app.models.category import Category
from app.models.users import User
from app.schemas.providers import ProviderCreate, ProviderUpdate, ProviderResponse
from app.core.dependencies import require_provider
from app.services.location_service import is_within_philippines, find_nearby_providers

router = APIRouter()


@router.post("/", response_model=ProviderResponse, dependencies=[Depends(require_provider)])
def create_provider(
    provider: ProviderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    if not is_within_philippines(provider.latitude, provider.longitude):
        raise HTTPException(status_code=400, detail="Provider location must be inside the Philippines")

    new_provider = Provider(
        owner_id=current_user.id,
        **provider.dict()
    )

    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)

    return new_provider


@router.get("/", response_model=list[ProviderResponse])
def get_providers(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return db.query(Provider).offset(offset).limit(limit).all()


@router.get("/nearby")
def get_nearby(
    lat: float,
    lng: float,
    radius: float = 10,
    db: Session = Depends(get_db)
):
    try:
        return find_nearby_providers(db, lat, lng, radius)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/map")
def get_providers_in_map(
    min_lat: float,
    max_lat: float,
    min_lng: float,
    max_lng: float,
    db: Session = Depends(get_db)
):
    providers = db.query(Provider).filter(
        Provider.latitude >= min_lat,
        Provider.latitude <= max_lat,
        Provider.longitude >= min_lng,
        Provider.longitude <= max_lng
    ).all()

    return providers


@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return provider


@router.get("/{provider_id}/profile")
def get_provider_profile(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    services = db.query(Service).filter(Service.provider_id == provider_id).all()

    categories = (
        db.query(Category)
        .join(Service, Service.category_id == Category.id)
        .filter(Service.provider_id == provider_id)
        .all()
    )

    return {
        "provider": provider,
        "services": services,
        "categories": categories,
        "rating": {
            "rating": provider.rating,
            "total_reviews": provider.total_reviews
        }
    }


@router.put("/{provider_id}", response_model=ProviderResponse, dependencies=[Depends(require_provider)])
def update_provider(
    provider_id: int,
    provider: ProviderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    db_provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not db_provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    if db_provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = provider.dict(exclude_unset=True)

    if "latitude" in update_data and "longitude" in update_data:
        if not is_within_philippines(update_data["latitude"], update_data["longitude"]):
            raise HTTPException(status_code=400, detail="Provider location must be inside the Philippines")

    for key, value in update_data.items():
        setattr(db_provider, key, value)

    db.commit()
    db.refresh(db_provider)

    return db_provider


@router.delete("/{provider_id}", dependencies=[Depends(require_provider)])
def delete_provider(
    provider_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    if provider.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(provider)
    db.commit()

    return {"message": "Provider deleted"}