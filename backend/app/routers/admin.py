from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.db import get_db
from app.models.users import User
from app.models.providers import Provider
from app.models.appointment import Appointment
from app.models.service import Service
from app.schemas.admin import PlatformOverview, RecentActivity, RecentUser, RecentAppointment
from app.schemas.users import UserResponse
from app.core.dependencies import require_admin

router = APIRouter(dependencies=[Depends(require_admin)])

@router.get("/overview", response_model=PlatformOverview)
def get_platform_overview(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_providers = db.query(Provider).count()
    total_appointments = db.query(Appointment).count()
    
    # Calculate total revenue from completed appointments
    revenue_result = (
        db.query(func.sum(Service.price))
        .select_from(Appointment)
        .join(Service, Appointment.service_id == Service.id)
        .filter(Appointment.status == "completed")
        .scalar()
    )
    total_revenue = float(revenue_result) if revenue_result else 0.0
    
    pending_approvals = db.query(User).filter(User.is_approved == False).count()
    
    return PlatformOverview(
        total_users=total_users,
        total_providers=total_providers,
        total_appointments=total_appointments,
        total_revenue=total_revenue,
        pending_approvals=pending_approvals
    )

@router.get("/recent-activity", response_model=RecentActivity)
def get_recent_activity(db: Session = Depends(get_db)):
    # Recent 5 users
    db_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
    recent_users = [
        RecentUser(
            id=u.id, 
            full_name=u.full_name, 
            email=u.email, 
            role=u.role, 
            created_at=u.created_at
        ) for u in db_users
    ]
    
    # Recent 5 appointments
    db_appointments = db.query(Appointment).order_by(Appointment.created_at.desc()).limit(5).all()
    recent_appointments = [
        RecentAppointment(
            id=a.id,
            service_name=a.service.name if a.service else "Unknown",
            provider_name=a.provider.shop_name if a.provider else "Unknown",
            customer_name=a.user.full_name if a.user else "Unknown",
            status=a.status,
            created_at=a.created_at
        ) for a in db_appointments
    ]
    
    return RecentActivity(
        recent_users=recent_users,
        recent_appointments=recent_appointments
    )

@router.get("/users/pending", response_model=List[UserResponse])
def get_pending_users(db: Session = Depends(get_db)):
    return db.query(User).filter(User.is_approved == False).all()
