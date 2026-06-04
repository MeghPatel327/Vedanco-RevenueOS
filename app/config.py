from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    baserow_api_token: str
    openrouter_api_key: str
    openrouter_model: str = "qwen/qwen3-8b"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

# Baserow Table IDs
TABLE_LEADS = 1009952
TABLE_APPOINTMENTS = 1009953
TABLE_ACTIVITIES = 1009954

# Lead Status Options (Single Select IDs)
LEAD_STATUS = {
    "New Lead": 6407606,
    "Qualified": 6407609,
    "Appointment Booked": 6407610,
    "Not Interested": 6407613
}

# Activity Type Options (Single Select IDs)
ACTIVITY_TYPES = {
    "Lead Created": 6407618,
    "AI Qualified": 6407619,
    "Appointment Booked": 6407620
}
