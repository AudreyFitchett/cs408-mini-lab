import requests
from django.conf import settings
from .models import Assignment, Course


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
        
    #gets all the courses from Canvas and stores them as a Course object
    def fetch_all_courses(canvas):
        next_url = f"{canvas.base_url}/api/v1/courses"
        while next_url:
            try:
                response = requests.get(next_url, headers=canvas._get_headers(), timeout=canvas.timeout)
                response.raise_for_status()
                data = response.json()

                for i in range(len(data)):
                    #filters out courses that can't be accessed
                    if("name" in data[i]):
                        #the goal of this is to not include courses from before the current semester
                        if("created_at" not in data and data[i]["created_at"] >= "2026-01-01"):
                            c = Course()
                            c.name = data[i]["name"]
                            c.id = data[i]["id"]
                            if("created_at" in data[i]):
                                c.date_created = data[i]["created_at"]
                                c.save()
                            else:
                                c.date_created = "undated"
                            

                if("next" in response.links):
                    next_url = response.links["next"]["url"]
                else:
                    next_url = None
            except requests.exceptions.RequestException as err:
                raise ExternalAPIServiceError(f"Error fetching paginated data: {err}")

    
    #grabs all the assignments from Canvas using the Course objects to find the url and 
    #stores them as an Assignment object
    def fetch_all_assignments(canvas):

        if(Course.objects.all() is None):
            ExternalApiClient.fetch_all_courses(canvas)
        courses = Course.objects.order_by("id")

        for course in courses:
            #filtering out courses that are not for this semester
            if(course.date_created != "undated" and course.date_created >= "2026-01-01"):
                next_url = f"{canvas.base_url}/api/v1/courses/{course.id}/assignments"
                while next_url:
                    try:
                        response = requests.get(next_url, headers=canvas._get_headers(), timeout=canvas.timeout)
                        response.raise_for_status()
                        data = response.json()

                        for i in range(len(data)):
                            if("name" in data[i]):
                                #Thecks if an the current json object is already an Assigment and skips it 
                                #if it is. It also forces to loop to move onto the next course, assuming that Canvas 
                                #assigments are ordered by most recently added, so anything that comes after an assigment
                                #that's already in the database is also already in the database.
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
                                    
                                    if("due_at" in data[i] and data[i]["due_at"] is not None):
                                        a.due_date = data[i]["due_at"]
                                    else:
                                        a.due_date = "undated"

                                    if("submission" in data[i] and data[i]["submission"] is not None):
                                        a.submitted = True

                                    a.save()
                        if(next_url is None):
                            break
                        elif("next" in response.links):
                            next_url = response.links["next"]["url"]
                        else:
                            next_url = None
                    except requests.exceptions.RequestException as err:
                        raise ExternalAPIServiceError(f"Error fetching paginated data: {err}")
