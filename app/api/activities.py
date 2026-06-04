from fastapi import APIRouter
from typing import List
from app.models.schemas import ActivityResponse
from app.services import baserow_service
from app.utils.logger import logger

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.get("/{lead_id}", response_model=List[ActivityResponse])
def get_activities(lead_id: int):
    """Get all activities for a specific lead."""
    logger.info(f"Endpoint hit: GET /activities/{lead_id}")
    activities = baserow_service.get_activities_for_lead(lead_id)
    return activities
