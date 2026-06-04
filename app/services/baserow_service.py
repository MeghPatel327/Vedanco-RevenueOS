from datetime import datetime
from typing import Dict, Any, List
from app.baserow.client import baserow_client
from app.config import TABLE_LEADS, TABLE_ACTIVITIES, TABLE_APPOINTMENTS, LEAD_STATUS, ACTIVITY_TYPES
from app.models.schemas import LeadCreate

def create_activity(lead_id: int, activity_type_name: str, description: str = "") -> Dict[str, Any]:
    activity_type_id = ACTIVITY_TYPES.get(activity_type_name)
    data = {
        "activity_type": activity_type_id,
        "description": description,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d"),
        "lead": [lead_id]
    }
    return baserow_client.create_row(TABLE_ACTIVITIES, data)

def create_lead(lead_in: LeadCreate) -> Dict[str, Any]:
    # Set status to New Lead
    data = lead_in.model_dump(exclude_unset=True)
    data["status"] = LEAD_STATUS["New Lead"]
    data["created_at"] = datetime.utcnow().strftime("%Y-%m-%d")
    
    # Create the lead
    lead = baserow_client.create_row(TABLE_LEADS, data)
    
    # Create the "Lead Created" activity
    create_activity(lead["id"], "Lead Created", "Lead was created in the system.")
    return lead

def get_leads(params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    response = baserow_client.get_rows(TABLE_LEADS, params)
    return response.get("results", [])

def get_lead_by_id(lead_id: int) -> Dict[str, Any]:
    return baserow_client.get_row(TABLE_LEADS, lead_id)

def update_lead_status(lead_id: int, status_name: str) -> Dict[str, Any]:
    status_id = LEAD_STATUS.get(status_name)
    if not status_id:
        raise ValueError(f"Invalid status name: {status_name}")
    data = {"status": status_id}
    return baserow_client.update_row(TABLE_LEADS, lead_id, data)

def create_appointment(lead_id: int, appointment_date: str, appointment_time: str) -> Dict[str, Any]:
    data = {
        "lead": [lead_id],
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "created_at": datetime.utcnow().strftime("%Y-%m-%d")
    }
    appointment = baserow_client.create_row(TABLE_APPOINTMENTS, data)
    
    # Update lead status
    update_lead_status(lead_id, "Appointment Booked")
    
    # Create activity
    create_activity(lead_id, "Appointment Booked", f"Appointment scheduled for {appointment_date} at {appointment_time}.")
    
    return appointment

def get_dashboard_metrics() -> Dict[str, Any]:
    # In a real scenario, you might want to paginate through all or use Baserow views/filters
    # For now, we'll fetch up to 100 or default limit and calculate.
    # To do it properly with Baserow, we can fetch count of rows using filters.
    
    # Get total leads
    total_response = baserow_client.get_rows(TABLE_LEADS, {"size": 1})
    total_leads = total_response.get("count", 0)
    
    # Get qualified leads
    qualified_response = baserow_client.get_rows(
        TABLE_LEADS, 
        {"size": 1, "filter__field_8860282__equal": LEAD_STATUS["Qualified"]}
    )
    qualified_leads = qualified_response.get("count", 0)
    
    # Get appointment booked leads
    appointment_response = baserow_client.get_rows(
        TABLE_LEADS, 
        {"size": 1, "filter__field_8860282__equal": LEAD_STATUS["Appointment Booked"]}
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
