import requests
from django.conf import settings
import json
from types import SimpleNamespace
from .models import Assignment, Course
from datetime import date, datetime
from django.http import JsonResponse, HttpResponseBadRequest


class ExternalAPIServiceError(Exception):
    """Custom exception for service-level errors."""
    pass

class ExternalApiClient:
    def __init__(canvas):
        canvas.base_url = settings.CANVAS_BASE_URL
        canvas.api_key = settings.CANVAS_API_TOKEN
        canvas.timeout = 5.0

    def _get_headers(canvas) -> dict:
        return {
            "Authorization": f"Bearer {canvas.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def fetch_items(canvas, category: str = None) -> list:
        endpoint = f"{canvas.base_url}/v1/items"
        params = {"category": category} if category else {}

        try:
            response = requests.get(
                endpoint,
                headers=canvas._get_headers(),
                params=params,
                timeout=canvas.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            raise ExternalAPIServiceError(f"API responded with status {response.status_code}: {err}")
        except requests.exceptions.RequestException as err:
            raise ExternalAPIServiceError(f"Network error while reaching external API: {err}")
        
    def fetch_all_courses(canvas) -> list:
        # all_courses = []
        next_url = f"{canvas.base_url}/api/v1/courses"

        while next_url:
            try:
                response = requests.get(next_url, headers=canvas._get_headers(), timeout=canvas.timeout)
                response.raise_for_status()
                data = response.json()

                # Extend result list with items from current page
                # this didn't work
                # all_courses.extend(data.get("results", []))
                #trying to get around access restricted items
                for i in range(len(data)):
                    if("name" in data[i]):
                        temp = json.loads(json.dumps(data[i]), object_hook=SimpleNamespace)
                        c = Course()
                        c.name = temp.name
                        c.id = temp.id
                        c.date_created = temp.created_at
                        c.save()
                        # all_courses.append(temp)
                        # all_courses.append(data[i]["name", "id", "end_at"])

                # Update next_url for the next iteration (None when no more pages)
                if("next" in response.links):
                    next_url = response.links["next"]["url"]
                else:
                    next_url = None
            except requests.exceptions.RequestException as err:
                raise ExternalAPIServiceError(f"Error fetching paginated data: {err}")

        # return all_courses
    
    def fetch_all_assignments(canvas) -> list:
        all_assignments = []
        all_courses = ExternalApiClient.fetch_all_courses(canvas)
        next_url = f"{canvas.base_url}/api/v1/courses/{all_courses[0].id}/assignments"

        for i in range(len(all_courses)):
            next_url = f"{canvas.base_url}/api/v1/courses/{all_courses[i].id}/assignments"
            if(all_courses[i].created_at is None or all_courses[i].created_at >= "2026-01-01"):
                while next_url:
                    try:
                        response = requests.get(next_url, headers=canvas._get_headers(), timeout=canvas.timeout)
                        response.raise_for_status()
                        data = response.json()

                        # Extend result list with items from current page
                        # this didn't work
                        # all_courses.extend(data.get("results", []))
                        #trying to get around access restricted items
                        for i in range(len(data)):
                            if("name" in data[i]):
                                temp = json.loads(json.dumps(data[i]), object_hook=SimpleNamespace)
                                all_assignments.append(temp)

                        # Update next_url for the next iteration (None when no more pages)
                        if("next" in response.links):
                            next_url = response.links["next"]["url"]
                        else:
                            next_url = None
                    except requests.exceptions.RequestException as err:
                        raise ExternalAPIServiceError(f"Error fetching paginated data: {err}")

        return all_assignments
    
   
    def create_item(canvas, payload: dict) -> dict:
        endpoint = f"{canvas.base_url}/v1/items"

        try:
            response = requests.post(
                endpoint,
                headers=canvas._get_headers(),
                json=payload,
                timeout=canvas.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            raise ExternalAPIServiceError(f"Failed to create item: {err}")