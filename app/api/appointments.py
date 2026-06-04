from fastapi import APIRouter, status
from app.models.schemas import AppointmentCreate, AppointmentResponse, AppointmentUpdate

from app.services import baserow_service
from app.utils.logger import logger

router = APIRouter(prefix="/appointment", tags=["Appointments"])

@router.get("s", response_model=list[AppointmentResponse])
def get_all_appointments():
    """Get all appointments."""
    logger.info("Endpoint hit: GET /appointments")
    return baserow_service.get_all_appointments()

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

@router.put("/{id}", response_model=AppointmentResponse)
def update_appointment(id: int, appointment_in: AppointmentUpdate):
    """Update a specific appointment by ID."""
    logger.info(f"Endpoint hit: PUT /appointment/{id}")
    appointment = baserow_service.update_appointment(id, appointment_in)
    return appointment

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(id: int):
    """Delete a specific appointment by ID."""
    logger.info(f"Endpoint hit: DELETE /appointment/{id}")
    baserow_service.delete_appointment(id)
    return None
