from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.service import Service
from app.models.providers import Provider
from app.models.category import Category


def search_services(
    db: Session,
    query: str | None = None,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None
):

    q = (
        db.query(Service)
        .join(Provider, Service.provider_id == Provider.id)
        .join(Category, Service.category_id == Category.id)
    )

    if query:
        q = q.filter(
            or_(
                Service.name.ilike(f"%{query}%"),
                Service.description.ilike(f"%{query}%"),
                Provider.shop_name.ilike(f"%{query}%")
            )
        )

    if category_id:
        q = q.filter(Service.category_id == category_id)

    if min_price is not None:
        q = q.filter(Service.price >= min_price)

    if max_price is not None:
        q = q.filter(Service.price <= max_price)

    return q.all()