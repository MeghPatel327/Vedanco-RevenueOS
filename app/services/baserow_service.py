from datetime import datetime
from typing import Dict, Any, List
from app.baserow.client import baserow_client
from app.config import settings, LEAD_STATUS, ACTIVITY_TYPES, LEAD_STATUS_FIELD_ID
from app.models.schemas import LeadCreate
from app.utils.logger import logger

def create_activity(lead_id: int, activity_type_name: str, description: str = "") -> Dict[str, Any]:
    """Create an activity for a lead in Baserow."""
    logger.info(f"Creating activity '{activity_type_name}' for lead {lead_id}")
    activity_type_id = ACTIVITY_TYPES.get(activity_type_name)
    data = {
        "activity_type": activity_type_id,
        "description": description,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d"),
        "lead": [lead_id]
    }
    return baserow_client.create_row(settings.baserow_table_activities, data)

def create_lead(lead_in: LeadCreate) -> Dict[str, Any]:
    """Create a new lead in Baserow and log an activity."""
    logger.info(f"Creating new lead: {lead_in.name}")
    # Set status to New Lead
    data = lead_in.model_dump(exclude_unset=True)
    data["status"] = LEAD_STATUS["New Lead"]
    data["created_at"] = datetime.utcnow().strftime("%Y-%m-%d")
    
    # Create the lead
    lead = baserow_client.create_row(settings.baserow_table_leads, data)
    
    # Create the "Lead Created" activity
    create_activity(lead["id"], "Lead Created", "Lead was created in the system.")
    return lead

def get_leads(params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Retrieve a list of leads from Baserow."""
    logger.info("Fetching leads from Baserow")
    response = baserow_client.get_rows(settings.baserow_table_leads, params)
    return response.get("results", [])

def get_lead_by_id(lead_id: int) -> Dict[str, Any]:
    """Retrieve a specific lead by its ID from Baserow."""
    logger.info(f"Fetching lead by ID: {lead_id}")
    return baserow_client.get_row(settings.baserow_table_leads, lead_id)

def update_lead_status(lead_id: int, status_name: str) -> Dict[str, Any]:
    """Update the status of a specific lead."""
    logger.info(f"Updating lead {lead_id} status to '{status_name}'")
    status_id = LEAD_STATUS.get(status_name)
    if not status_id:
        raise ValueError(f"Invalid status name: {status_name}")
    data = {"status": status_id}
    return baserow_client.update_row(settings.baserow_table_leads, lead_id, data)

def create_appointment(lead_id: int, appointment_date: str, appointment_time: str) -> Dict[str, Any]:
    """Create an appointment for a lead and update their status."""
    logger.info(f"Creating appointment for lead {lead_id} on {appointment_date} at {appointment_time}")
    data = {
        "lead": [lead_id],
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "created_at": datetime.utcnow().strftime("%Y-%m-%d")
    }
    appointment = baserow_client.create_row(settings.baserow_table_appointments, data)
    
    # Update lead status
    update_lead_status(lead_id, "Appointment Booked")
    
    # Create activity
    create_activity(lead_id, "Appointment Booked", f"Appointment scheduled for {appointment_date} at {appointment_time}.")
    
    return appointment

def get_dashboard_metrics() -> Dict[str, Any]:
    """Fetch dashboard metrics including total leads, qualified leads, and conversion rate."""
    logger.info("Fetching dashboard metrics")
    
    # Get total leads
    total_response = baserow_client.get_rows(settings.baserow_table_leads, {"size": 1})
    total_leads = total_response.get("count", 0)
    
    # Baserow single_select fields require filter type "single_select_equal"
    # The filter key format is: filter__field_{FIELD_ID}__single_select_equal
    # The value must be the display text of the option (e.g., "Qualified")
    filter_key = f"filter__field_{LEAD_STATUS_FIELD_ID}__single_select_equal"
    
    # Get qualified leads
    qualified_response = baserow_client.get_rows(
        settings.baserow_table_leads, 
        {"size": 1, filter_key: "Qualified"}
    )
    qualified_leads = qualified_response.get("count", 0)
    
    # Get appointment booked leads
    appointment_response = baserow_client.get_rows(
        settings.baserow_table_leads, 
        {"size": 1, filter_key: "Appointment Booked"}
    )
    appointment_leads = appointment_response.get("count", 0)
    
    conversion_rate = 0.0
    if total_leads > 0:
        conversion_rate = (appointment_leads / total_leads) * 100
        
    return {
        "total_leads": total_leads,
        "qualified_leads": qualified_leads,
        "appointment_booked_leads": appointment_leads,
        "conversion_rate": round(conversion_rate, 2)
    }

