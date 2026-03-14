from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.category import Category
from app.models.service import Service
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.service import ServiceResponse
from app.core.dependencies import require_admin, get_current_user

router = APIRouter(dependencies=[Depends(require_admin)])


@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return db.query(Category).offset(offset).limit(limit).all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get(
    "/{category_id}/services",
    response_model=list[ServiceResponse],
    dependencies=[Depends(get_current_user)]
)
def get_category_services(
    category_id: int,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    services = db.query(Service).filter(
        Service.category_id == category_id
    ).offset(offset).limit(limit).all()

    return services


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db_category.name = category.name
    db.commit()
    db.refresh(db_category)

    return db_category


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(db_category)
    db.commit()

    return {"message": "Category deleted"}