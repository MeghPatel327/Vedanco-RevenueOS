from fastapi import APIRouter, HTTPException, status
from typing import Any, Dict
from app.services import baserow_service, openrouter_service
from requests.exceptions import RequestException

router = APIRouter(prefix="/qualify", tags=["Qualification"])

@router.post("/{lead_id}", response_model=Dict[str, Any])
def qualify_lead_endpoint(lead_id: int):
    try:
        # Fetch lead from Baserow
        lead = baserow_service.get_lead_by_id(lead_id)
    except RequestException as e:
        if e.response is not None and e.response.status_code == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Baserow API error: {str(e)}")

    # Send lead information to OpenRouter
    ai_result = openrouter_service.qualify_lead(lead)
    
    new_status = ai_result.get("status", "Not Interested")
    reason = ai_result.get("reason", "No reason provided.")
    
    try:
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
    except RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Baserow API error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
