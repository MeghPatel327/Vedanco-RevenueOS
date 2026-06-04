from fastapi import APIRouter, HTTPException, status
from typing import Any, Dict
from app.models.schemas import AppointmentCreate
from app.services import baserow_service
from requests.exceptions import RequestException

router = APIRouter(prefix="/appointment", tags=["Appointments"])

@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def book_appointment(appointment_in: AppointmentCreate):
    try:
        # Check if lead exists first
        try:
            baserow_service.get_lead_by_id(appointment_in.lead_id)
        except RequestException as e:
            if e.response is not None and e.response.status_code == 404:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
            raise e
        
        # Create appointment and update lead
        appointment = baserow_service.create_appointment(
            lead_id=appointment_in.lead_id,
            appointment_date=appointment_in.appointment_date,
            appointment_time=appointment_in.appointment_time
        )
        return appointment
    except RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Baserow API error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
