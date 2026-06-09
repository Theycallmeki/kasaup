from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PlatformOverview(BaseModel):
    total_users: int
    total_providers: int
    total_appointments: int
    total_revenue: float
    pending_approvals: int

class RecentUser(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: str
    role: str
    created_at: Optional[datetime] = None

class RecentAppointment(BaseModel):
    id: int
    service_name: str
    provider_name: str
    customer_name: str
    status: str
    created_at: Optional[datetime] = None

class RecentActivity(BaseModel):
    recent_users: List[RecentUser]
    recent_appointments: List[RecentAppointment]
