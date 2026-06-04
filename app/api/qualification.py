from fastapi import APIRouter
from app.models.schemas import QualificationResponse
from app.services import baserow_service, openrouter_service
from app.utils.logger import logger

router = APIRouter(prefix="/qualify", tags=["Qualification"])

@router.post("/{lead_id}", response_model=QualificationResponse)
def qualify_lead_endpoint(lead_id: int):
    """Qualify a lead using AI and update their status."""
    logger.info(f"Endpoint hit: POST /qualify/{lead_id}")
    
    # Fetch lead from Baserow
    lead = baserow_service.get_lead_by_id(lead_id)

    # Send lead information to OpenRouter
    ai_result = openrouter_service.qualify_lead(lead)
    
    new_status = ai_result.get("status", "Not Interested")
    reason = ai_result.get("reason", "No reason provided.")
    
    # Update lead status
    updated_lead = baserow_service.update_lead_status(lead_id, new_status)
    
    # Create activity
    baserow_service.create_activity(
        lead_id=lead_id,
        activity_type_name="AI Qualified",
        description=f"AI determined status: {new_status}. Reason: {reason}"
    )
    
    return {
        "message": "Lead qualified successfully",
        "new_status": new_status,
        "reason": reason,
        "lead": updated_lead
    }
