from fastapi import APIRouter
from app.api import leads, qualification, appointments, dashboard

api_router = APIRouter()

api_router.include_router(leads.router)
api_router.include_router(leads.leads_router)
api_router.include_router(qualification.router)
api_router.include_router(appointments.router)
api_router.include_router(dashboard.router)
