from fastapi import APIRouter
from app.models.schemas import DashboardMetrics
from app.services import baserow_service
from app.utils.logger import logger

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardMetrics)
def get_dashboard():
    """Get dashboard metrics for leads and conversion rates."""
    logger.info("Endpoint hit: GET /dashboard")
    metrics = baserow_service.get_dashboard_metrics()
    return metrics
