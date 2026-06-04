from fastapi import APIRouter, HTTPException, status
from app.models.schemas import DashboardMetrics
from app.services import baserow_service
from requests.exceptions import RequestException

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", response_model=DashboardMetrics)
def get_dashboard():
    try:
        metrics = baserow_service.get_dashboard_metrics()
        return metrics
    except RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Baserow API error: {str(e)}")
