from sqlalchemy.orm import Session
from app.models.providers import Provider


def get_providers_in_bounds(
    db: Session,
    min_lat: float,
    max_lat: float,
    min_lng: float,
    max_lng: float,
):

    providers = db.query(Provider).filter(
        Provider.latitude >= min_lat,
        Provider.latitude <= max_lat,
        Provider.longitude >= min_lng,
        Provider.longitude <= max_lng,
        Provider.is_verified == True
    ).all()

    return providers