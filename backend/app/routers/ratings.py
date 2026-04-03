from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.review import Review
from app.models.appointment import Appointment
from app.models.providers import Provider
from app.schemas.review import ReviewCreate, ReviewUpdate, Review as ReviewSchema
from app.core.dependencies import get_current_user
from app.models.users import User

router = APIRouter()


@router.post("/", response_model=ReviewSchema)
def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if review_in.appointment_id:
        appointment = db.query(Appointment).filter(
            Appointment.id == review_in.appointment_id,
            Appointment.user_id == current_user.id
        ).first()
        
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found or does not belong to you")
        
        if appointment.status != "completed":
            raise HTTPException(status_code=400, detail="Cannot review an appointment that is not completed")
        
        existing_review = db.query(Review).filter(Review.appointment_id == appointment.id).first()
        if existing_review:
            raise HTTPException(status_code=400, detail="Appointment already reviewed")
        
        provider_id = appointment.provider_id
    else:
        raise HTTPException(status_code=400, detail="appointment_id is required for verified reviews")

    db_review = Review(
        appointment_id=review_in.appointment_id,
        user_id=current_user.id,
        provider_id=provider_id,
        rating=review_in.rating,
        comment=review_in.comment
    )
    db.add(db_review)
    
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if provider:
        total_rating = (provider.rating * provider.total_reviews) + review_in.rating
        provider.total_reviews += 1
        provider.rating = total_rating / provider.total_reviews
    
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/provider/{provider_id}/", response_model=List[ReviewSchema])
def get_provider_reviews(provider_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.provider_id == provider_id).all()


@router.get("/me/", response_model=List[ReviewSchema])
def get_my_reviews(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Review).filter(Review.user_id == current_user.id).all()


@router.put("/{review_id}/", response_model=ReviewSchema)
def update_review(
    review_id: int,
    review_in: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_review = db.query(Review).filter(Review.id == review_id, Review.user_id == current_user.id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    provider = db.query(Provider).filter(Provider.id == db_review.provider_id).first()
    
    if review_in.rating is not None and provider:
        old_total = provider.rating * provider.total_reviews
        new_total = old_total - db_review.rating + review_in.rating
        provider.rating = new_total / provider.total_reviews
        db_review.rating = review_in.rating
        
    if review_in.comment is not None:
        db_review.comment = review_in.comment
        
    db.commit()
    db.refresh(db_review)
    return db_review


@router.delete("/{review_id}/")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_review = db.query(Review).filter(Review.id == review_id, Review.user_id == current_user.id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    provider = db.query(Provider).filter(Provider.id == db_review.provider_id).first()
    if provider:
        old_total = provider.rating * provider.total_reviews
        provider.total_reviews -= 1
        if provider.total_reviews > 0:
            provider.rating = (old_total - db_review.rating) / provider.total_reviews
        else:
            provider.rating = 0
            
    db.delete(db_review)
    db.commit()
    return {"message": "Review deleted successfully"}
