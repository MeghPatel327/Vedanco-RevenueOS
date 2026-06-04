import json
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    openrouter_api_key: str
    openrouter_model: str
    ai_provider: str
    ai_model: str
    ai_temperature: float
    ai_max_tokens: int
    
    baserow_api_token: str
    baserow_base_url: str
    
    app_name: str
    debug: bool
    
    # We will populate these from the JSON file dynamically
    baserow_table_leads: int = 0
    baserow_table_appointments: int = 0
    baserow_table_activities: int = 0

    model_config = SettingsConfigDict(env_file=str(PROJECT_ROOT / ".env"), extra="ignore")

settings = Settings()

# --- CRM Structure Parsing ---
CRM_STRUCTURE_FILE = PROJECT_ROOT / "CRM_data_structure.json"

try:
    with open(CRM_STRUCTURE_FILE, "r") as f:
        crm_data = json.load(f)
except FileNotFoundError:
    crm_data = {"tables": []}

# Extract Table IDs dynamically
TABLES = {table["name"]: table["id"] for table in crm_data.get("tables", [])}

settings.baserow_table_leads = TABLES.get("Leads", 0)
settings.baserow_table_appointments = TABLES.get("Appointments", 0)
settings.baserow_table_activities = TABLES.get("Activities", 0)

# Extract Status and Activity Options dynamically
LEAD_STATUS = {}
ACTIVITY_TYPES = {}
LEAD_STATUS_FIELD_ID = None

for table in crm_data.get("tables", []):
    if table["name"] == "Leads":
        for field in table.get("fields", []):
            if field["name"] == "status":
                LEAD_STATUS_FIELD_ID = field.get("id")
                LEAD_STATUS = {opt["value"]: opt["id"] for opt in field.get("options", [])}
    
    if table["name"] == "Activities":
        for field in table.get("fields", []):
            if field["name"] == "activity_type":
                ACTIVITY_TYPES = {opt["value"]: opt["id"] for opt in field.get("options", [])}
