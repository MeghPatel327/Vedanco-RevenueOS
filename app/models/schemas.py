from pydantic import BaseModel, EmailStr, Field, field_validator
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

class LeadUpdate(BaseModel):
    """Schema for updating an existing lead."""
    name: Optional[str] = Field(None, example="John Doe")
    email: Optional[EmailStr] = Field(None, example="john@example.com")
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

class AppointmentUpdate(BaseModel):
    """Schema for updating an appointment."""
    appointment_date: Optional[str] = Field(None, example="2024-05-21")
    appointment_time: Optional[str] = Field(None, example="15:00")

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
    status: Optional[str] = None
    created_at: Optional[str] = None
    
    @field_validator("source", "status", mode="before")
    @classmethod
    def extract_single_select_value(cls, v):
        """Baserow returns single_select fields as dicts like {'id': 123, 'value': 'Website', 'color': 'green'}.
        Extract just the display value string."""
        if isinstance(v, dict):
            return v.get("value")
        return v
    
    class Config:
        extra = "ignore"  # Ignore extra fields from Baserow

class AppointmentResponse(BaseModel):
    """Schema for returning appointment data."""
    id: int
    lead: List[Any] = []
    appointment_date: str
    appointment_time: str
    created_at: str

    class Config:
        extra = "ignore"

class ActivityResponse(BaseModel):
    """Schema for returning activity data."""
    id: int
    activity_type: Optional[str] = None
    description: Optional[str] = None
    timestamp: str
    lead: List[Any] = []
    
    @field_validator("activity_type", mode="before")
    @classmethod
    def extract_single_select_value(cls, v):
        """Extract just the display value string."""
        if isinstance(v, dict):
            return v.get("value")
        return v
        
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
