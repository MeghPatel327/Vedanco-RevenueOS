import requests
from typing import Dict, Any, Optional, List
from app.config import settings

class BaserowClient:
    BASE_URL = "https://api.baserow.io/api"

    def __init__(self):
        self.headers = {
            "Authorization": f"Token {settings.baserow_api_token}",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data, params=params)
        response.raise_for_status()
        if method != "DELETE":
            return response.json()
        return None

    def create_row(self, table_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        endpoint = f"/database/rows/table/{table_id}/?user_field_names=true"
        return self._request("POST", endpoint, data=data)

    def get_rows(self, table_id: int, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        endpoint = f"/database/rows/table/{table_id}/?user_field_names=true"
        return self._request("GET", endpoint, params=params)

    def get_row(self, table_id: int, row_id: int) -> Dict[str, Any]:
        endpoint = f"/database/rows/table/{table_id}/{row_id}/?user_field_names=true"
        return self._request("GET", endpoint)

    def update_row(self, table_id: int, row_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        endpoint = f"/database/rows/table/{table_id}/{row_id}/?user_field_names=true"
        return self._request("PATCH", endpoint, data=data)

baserow_client = BaserowClient()
