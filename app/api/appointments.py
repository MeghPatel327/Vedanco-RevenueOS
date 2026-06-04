from fastapi import APIRouter, status
from app.models.schemas import AppointmentCreate, AppointmentResponse
from app.services import baserow_service
from app.utils.logger import logger

router = APIRouter(prefix="/appointment", tags=["Appointments"])

@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def book_appointment(appointment_in: AppointmentCreate):
    """Book an appointment for a lead."""
    logger.info(f"Endpoint hit: POST /appointment for lead {appointment_in.lead_id}")
    
    # Check if lead exists first
    baserow_service.get_lead_by_id(appointment_in.lead_id)
    
    # Create appointment and update lead
    appointment = baserow_service.create_appointment(
        lead_id=appointment_in.lead_id,
        appointment_date=appointment_in.appointment_date,
        appointment_time=appointment_in.appointment_time
    )
    return appointment
