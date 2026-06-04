from datetime import datetime
from typing import Dict, Any, List
from app.baserow.client import baserow_client
from app.config import settings, LEAD_STATUS, ACTIVITY_TYPES, LEAD_STATUS_FIELD_ID
from app.models.schemas import LeadCreate, LeadUpdate, AppointmentUpdate
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
    
    # Use json filters with the status option IDs instead of query string
    import json
    
    qualified_id = str(LEAD_STATUS.get("Qualified", ""))
    qualified_filter = json.dumps({
        "filter_type": "AND",
        "filters": [{"type": "single_select_equal", "field": "status", "value": qualified_id}]
    })
    
    qualified_response = baserow_client.get_rows(
        settings.baserow_table_leads, 
        {"size": 1, "filters": qualified_filter}
    )
    qualified_leads = qualified_response.get("count", 0)
    
    appointment_id = str(LEAD_STATUS.get("Appointment Booked", ""))
    appointment_filter = json.dumps({
        "filter_type": "AND",
        "filters": [{"type": "single_select_equal", "field": "status", "value": appointment_id}]
    })
    
    appointment_response = baserow_client.get_rows(
        settings.baserow_table_leads, 
        {"size": 1, "filters": appointment_filter}
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

def update_lead(lead_id: int, lead_in: LeadUpdate) -> Dict[str, Any]:
    """Update an existing lead in Baserow and log an activity."""
    logger.info(f"Updating lead ID: {lead_id}")
    data = lead_in.model_dump(exclude_unset=True)
    if not data:
        return baserow_client.get_row(settings.baserow_table_leads, lead_id)
        
    lead = baserow_client.update_row(settings.baserow_table_leads, lead_id, data)
    create_activity(lead_id, "Status Updated", "Lead information was updated.")
    return lead

def delete_lead(lead_id: int) -> None:
    """Delete a lead from Baserow."""
    logger.info(f"Deleting lead ID: {lead_id}")
    baserow_client.delete_row(settings.baserow_table_leads, lead_id)

def update_appointment(appointment_id: int, appt_in: AppointmentUpdate) -> Dict[str, Any]:
    """Update an existing appointment in Baserow."""
    logger.info(f"Updating appointment ID: {appointment_id}")
    data = appt_in.model_dump(exclude_unset=True)
    if not data:
        return baserow_client.get_row(settings.baserow_table_appointments, appointment_id)
        
    appointment = baserow_client.update_row(settings.baserow_table_appointments, appointment_id, data)
    
    # Log an activity if we have the lead ID
    lead_list = appointment.get("lead", [])
    if lead_list and isinstance(lead_list, list) and len(lead_list) > 0:
        lead_id = lead_list[0].get("id")
        create_activity(lead_id, "Status Updated", "Appointment details were updated.")
        
    return appointment

def get_all_appointments() -> list[Dict[str, Any]]:
    """Retrieve all appointments from Baserow."""
    logger.info("Fetching all appointments")
    response = baserow_client.get_rows(settings.baserow_table_appointments)
    return response.get("results", [])

def delete_appointment(appointment_id: int) -> None:
    """Delete an appointment from Baserow."""
    logger.info(f"Deleting appointment ID: {appointment_id}")
    baserow_client.delete_row(settings.baserow_table_appointments, appointment_id)

def get_activities_for_lead(lead_id: int) -> List[Dict[str, Any]]:
    """Retrieve all activities for a specific lead."""
    logger.info(f"Fetching activities for lead ID: {lead_id}")
    # Assuming the linked row field is named 'lead'
    filter_key = "filter__field_lead__link_row_has" 
    # Alternatively, use standard text search or other method if field ID is known
    # If the above fails, you may need the exact field ID for the link row.
    # We will try a simple query, or fetch all and filter locally for MVP if needed.
    # To be safe and since Baserow API filters can be tricky, we'll try 'search' if link_row_has fails,
    # but the recommended way is using JSON filters:
    import json
    filter_json = json.dumps({
        "filter_type": "AND",
        "filters": [{"type": "link_row_has", "field": "lead", "value": str(lead_id)}]
    })
    params = {
        "filters": filter_json,
        "order_by": "-timestamp"
    }
    response = baserow_client.get_rows(settings.baserow_table_activities, params)
    return response.get("results", [])
