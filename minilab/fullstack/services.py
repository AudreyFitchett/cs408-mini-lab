import requests
from django.conf import settings
import json
from types import SimpleNamespace
from .models import Assignment, Course
import asyncio
import aiohttp
from datetime import date, datetime
from django.http import JsonResponse, HttpResponseBadRequest


class ExternalAPIServiceError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self) -> str:
        return self.message
    

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
        #async with aiohttp.ClientSession() as session:
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
                        #skip over old courses
                        if("created_at" not in data or data[i]["created_at"] >= "2026-01-01"):
                            c = Course()
                            c.name = data[i]["name"]
                            c.id = data[i]["id"]
                            c.date_created = data[i]["created at"]
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
    
    def fetch_all_assignments(canvas):

        if(Course.objects.all() is None):
            ExternalApiClient.fetch_all_courses(canvas)
        courses = Course.objects.order_by("id")

        for course in courses:
            #async with aiohttp.ClientSession() as session:
                next_url = f"{canvas.base_url}/api/v1/courses/{course.id}/assignments"
                #async with session.
                if(course.date_created is None or course.date_created >= "2026-01-01"):
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
                                    #thinking that if like the name and url matches an object already in the db
                                    #can use that as a stopping point (assuming canvas orders assigments by date)
                                    try:
                                        Assignment.objects.get(html_url = data[i]["html_url"])
                                        Assignment.objects.get(name = data[i]["name"])
                                        next_url = None
                                        break
                                    except Assignment.DoesNotExist:
                                        a = Assignment()
                                        a.name = data[i]["name"]
                                        a.course_id = data[i]["course_id"]
                                        a.course = course
                                        a.html_url = data[i]["html_url"]
                                        #TODO: format the date correctly under else
                                        
                                        if("due_at" in data[i] and data[i]["due_at"] is not None):
                                            a.due_date = data[i]["due_at"]
                                        else:
                                            a.due_date = "undated"

                                        if("submission" in data[i] and data[i]["submission"] is not None):
                                            a.submitted = True

                                        a.save()

                            # Update next_url for the next iteration (None when no more pages)
                            if(next_url is None):
                                break
                            elif("next" in response.links):
                                next_url = response.links["next"]["url"]
                            else:
                                next_url = None
                        except requests.exceptions.RequestException as err:
                            raise ExternalAPIServiceError(f"Error fetching paginated data: {err}")

    # async def fetch_course_assignments(canvas, course_id):

    #     if(Course.objects.all() is None):
    #         raise Exception("There are no courses")
        
    #     course = Course.objects.filter("course_id")

    #     if(course is None):
    #         raise Exception(f"There is not course with id: {course_id}")
        
    #     async with aiohttp.ClientSession() as session:
    #         next_url = f"{canvas.base_url}/api/v1/courses/{course_id}/assignments"
    #         async with session.request(next_url, headers=canvas._get_headers(), timeout=canvas.timeout) as response:
    #             if(course.date_created is None or course.date_created >= "2026-01-01"):
    #                 while next_url:
    #                     try:
    #                         #response = requests.get(next_url, headers=canvas._get_headers(), timeout=canvas.timeout)
    #                         response.raise_for_status()
    #                         data = await response.json()

    #                         # Extend result list with items from current page
    #                         # this didn't work
    #                         # all_courses.extend(data.get("results", []))
    #                         #trying to get around access restricted items
    #                         for i in range(len(data)):
    #                             if("name" in data[i]):
    #                                 temp = json.loads(json.dumps(data[i]), object_hook=SimpleNamespace)
    #                                 a = Assignment()
    #                                 a.name = temp.name
    #                                 a.course_id = temp.course_id
    #                                 a.html_url = temp.html_url
    #                                 #TODO: format the date correctly under else
    #                                 if(hasattr(temp, "due_at") and temp.due_at is not None):
    #                                     a.due_date = temp.due_at
    #                                 else:
    #                                     a.due_date = "2027-01-01"

    #                                 if(hasattr(temp, "submission") and temp.submission is not None):
    #                                     a.submitted = True

    #                                 a.save()

    #                         # Update next_url for the next iteration (None when no more pages)
    #                         if("next" in response.links):
    #                             next_url = response.links["next"]["url"]
    #                         else:
    #                             next_url = None
    #                     except requests.exceptions.RequestException as err:
    #                         raise ExternalAPIServiceError(f"Error fetching paginated data: {err}")
    
   
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