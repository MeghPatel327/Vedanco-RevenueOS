from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any, List
from datetime import date

# Request Models
class LeadCreate(BaseModel):
    """Schema for creating a new lead."""
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    phone: Optional[str] = Field(None, example="+1234567890")
    company: Optional[str] = Field(None, example="Acme Corp")
    source: Optional[str] = Field(None, example="Website")
    service: Optional[str] = Field(None, example="Consulting")
    notes: Optional[str] = Field(None, example="Interested in pricing.")

class AppointmentCreate(BaseModel):
    """Schema for booking an appointment."""
    lead_id: int = Field(..., example=1)
    appointment_date: str = Field(..., example="2024-05-20")
    appointment_time: str = Field(..., example="14:30")

# Response Models
class LeadResponse(BaseModel):
    """Schema for returning lead data."""
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    service: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[Any] = None # Assuming Baserow returns an object or int
    created_at: Optional[str] = None
    
    class Config:
        extra = "ignore" # Ignore extra fields from Baserow

class AppointmentResponse(BaseModel):
    """Schema for returning appointment data."""
    id: int
    lead: List[Any] = []
    appointment_date: str
    appointment_time: str
    created_at: str

    class Config:
        extra = "ignore"

class QualificationResponse(BaseModel):
    """Schema for returning qualification results."""
    message: str
    new_status: str
    reason: str
    lead: LeadResponse

class DashboardMetrics(BaseModel):
    """Schema for returning dashboard metrics."""
    total_leads: int
    qualified_leads: int
    appointment_booked_leads: int
    conversion_rate: float

class ErrorResponse(BaseModel):
    """Schema for standard error responses."""
    detail: str
