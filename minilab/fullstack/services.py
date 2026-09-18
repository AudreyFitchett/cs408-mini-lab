import requests
from django.conf import settings

class ExternalAPIServiceError(Exception):
    """Custom exception for service-level errors."""
    pass

class ExternalApiClient:
    def __init__(self):
        self.base_url = settings.EXTERNAL_API_BASE_URL
        self.api_key = settings.EXTERNAL_API_KEY
        self.timeout = 5.0

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def fetch_items(self, category: str = None) -> list:
        endpoint = f"{self.base_url}/v1/items"
        params = {"category": category} if category else {}

        try:
            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            raise ExternalAPIServiceError(f"API responded with status {response.status_code}: {err}")
        except requests.exceptions.RequestException as err:
            raise ExternalAPIServiceError(f"Network error while reaching external API: {err}")

    def create_item(self, payload: dict) -> dict:
        endpoint = f"{self.base_url}/v1/items"

        try:
            response = requests.post(
                endpoint,
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            raise ExternalAPIServiceError(f"Failed to create item: {err}")