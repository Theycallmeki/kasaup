from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.providers import Provider
from app.models.users import User
from app.schemas.providers import ProviderCreate, ProviderUpdate, ProviderResponse
from app.core.dependencies import require_provider

router = APIRouter(dependencies=[Depends(require_provider)])


@router.post("/", response_model=ProviderResponse)
def create_provider(
    provider: ProviderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_provider)
):
    new_provider = Provider(
        owner_id=current_user.id,
        **provider.dict()
    )

    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)

    return new_provider


@router.get("/", response_model=list[ProviderResponse])
def get_providers(db: Session = Depends(get_db)):
    return db.query(Provider).all()


@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()

    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return provider


@router.put("/{provider_id}", response_model=ProviderResponse)
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

    for key, value in provider.dict().items():
        setattr(db_provider, key, value)

    db.commit()
    db.refresh(db_provider)

    return db_provider


@router.delete("/{provider_id}")
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