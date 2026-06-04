from fastapi import APIRouter, status
from typing import List
from app.models.schemas import LeadCreate, LeadResponse, LeadUpdate, ErrorResponse
from app.services import baserow_service
from app.utils.logger import logger

router = APIRouter(prefix="/lead", tags=["Leads"])
leads_router = APIRouter(prefix="/leads", tags=["Leads"])

@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(lead_in: LeadCreate):
    """Create a new lead."""
    logger.info("Endpoint hit: POST /lead")
    lead = baserow_service.create_lead(lead_in)
    return lead

@leads_router.get("", response_model=List[LeadResponse])
def get_leads():
    """Get all leads."""
    logger.info("Endpoint hit: GET /leads")
    leads = baserow_service.get_leads()
    return leads

@router.get("/{id}", response_model=LeadResponse)
def get_lead_by_id(id: int):
    """Get a specific lead by ID."""
    logger.info(f"Endpoint hit: GET /lead/{id}")
    lead = baserow_service.get_lead_by_id(id)
    return lead

@router.put("/{id}", response_model=LeadResponse)
def update_lead(id: int, lead_in: LeadUpdate):
    """Update a specific lead by ID."""
    logger.info(f"Endpoint hit: PUT /lead/{id}")
    lead = baserow_service.update_lead(id, lead_in)
    return lead

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(id: int):
    """Delete a specific lead by ID."""
    logger.info(f"Endpoint hit: DELETE /lead/{id}")
    baserow_service.delete_lead(id)
    return None
