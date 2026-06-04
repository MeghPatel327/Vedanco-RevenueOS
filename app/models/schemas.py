from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from datetime import date

class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    service: Optional[str] = None
    notes: Optional[str] = None

class AppointmentCreate(BaseModel):
    lead_id: int
    appointment_date: str # YYYY-MM-DD
    appointment_time: str # HH:MM

class DashboardMetrics(BaseModel):
    total_leads: int
    qualified_leads: int
    appointment_booked_leads: int
    conversion_rate: float
