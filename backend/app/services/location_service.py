import math
from sqlalchemy.orm import Session
from app.models.providers import Provider

PH_MIN_LAT = 4.5
PH_MAX_LAT = 21.5

PH_MIN_LNG = 116
PH_MAX_LNG = 127


def is_within_philippines(lat: float, lng: float) -> bool:
    return (
        PH_MIN_LAT <= lat <= PH_MAX_LAT and
        PH_MIN_LNG <= lng <= PH_MAX_LNG
    )


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def find_nearby_providers(db: Session, lat: float, lng: float, radius: float):
    if not is_within_philippines(lat, lng):
        raise ValueError("Search location must be inside the Philippines")

    lat_range = radius / 111
    lng_range = radius / (111 * math.cos(math.radians(lat)))

    providers = db.query(Provider).filter(
        Provider.latitude.between(lat - lat_range, lat + lat_range),
        Provider.longitude.between(lng - lng_range, lng + lng_range)
    ).all()

    results = []

    for provider in providers:
        if provider.latitude is None or provider.longitude is None:
            continue

        distance = haversine_distance(lat, lng, provider.latitude, provider.longitude)

        if distance <= radius:
            results.append({
                "id": provider.id,
                "name": provider.name,
                "latitude": provider.latitude,
                "longitude": provider.longitude,
                "distance_km": round(distance, 2)
            })

    results.sort(key=lambda x: x["distance_km"])

    return results