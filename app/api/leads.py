from fastapi import APIRouter, HTTPException, status
from typing import Any, Dict, List
from app.models.schemas import LeadCreate
from app.services import baserow_service
from requests.exceptions import RequestException

router = APIRouter(prefix="/lead", tags=["Leads"])
leads_router = APIRouter(prefix="/leads", tags=["Leads"])

@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def create_lead(lead_in: LeadCreate):
    try:
        lead = baserow_service.create_lead(lead_in)
        return lead
    except RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Baserow API error: {str(e)}")

@leads_router.get("", response_model=List[Dict[str, Any]])
def get_leads():
    try:
        leads = baserow_service.get_leads()
        return leads
    except RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Baserow API error: {str(e)}")

@router.get("/{id}", response_model=Dict[str, Any])
def get_lead_by_id(id: int):
    try:
        lead = baserow_service.get_lead_by_id(id)
        return lead
    except RequestException as e:
        # Check if it's a 404 from Baserow
        if e.response is not None and e.response.status_code == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Baserow API error: {str(e)}")
