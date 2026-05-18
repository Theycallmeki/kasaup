from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.models.providers import Provider
from app.models.category import Category
from app.models.appointment import Appointment
from app.models.review import Review

router = APIRouter()

@router.get("/landing")
def get_landing_stats(db: Session = Depends(get_db)):
    providers_count = db.query(Provider).count()
    categories_count = db.query(Category).count()
    
    # Jobs completed
    jobs_completed = db.query(Appointment).filter(Appointment.status == "completed").count()
    
    # Average rating
    avg_rating_result = db.query(func.avg(Review.rating)).scalar()
    avg_rating = round(avg_rating_result, 1) if avg_rating_result else 0.0

    return {
        "active_providers": providers_count,
        "categories_count": categories_count,
        "jobs_completed": jobs_completed,
        "average_rating": avg_rating
    }
