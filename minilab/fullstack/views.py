from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Assignment, Course
from django.views.generic import ListView
import django_tables2 as tables
from rest_framework import serializers
from django.http import Http404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.http import JsonResponse
from django.views import View
from .services import ExternalApiClient, ExternalAPIServiceError
from django_tables2 import SingleTableView
from .tables import AssignmentTable

# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("index.html")
#     context = {"latest_question_list": latest_question_list}
#     return HttpResponse(template.render(context, request))

class IndexView(generic.ListView):
    template_name = "index.html"

    def get_queryset(self):
        """Return the last five published questions."""
        return Assignment.objects.order_by("course_id")[:5]

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "detail.html", {"question": question})
    
class DetailView(generic.DetailView):
    model = Assignment
    template_name = "detail.html"




# def assignments(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("assignments.html")
#     context = {"latest_question_list": latest_question_list}
#     return HttpResponse(template.render(context, request))

# def assignments(request):
#     client = ExternalApiClient()
#     error_message = None
#     assignments = Assignment.objects.order_by("course_id")
#     courses = Course.objects.order_by("id")

#     try:
#         # Calls the external API service method created earlier
#         #assignments = client.fetch_all_assignments()
#         if(not Course.objects.exists()):
#             client.fetch_all_courses()
#         #always check for new assignments
#         client.fetch_all_assignments()
#         assignments = Assignment.objects.order_by("course_id")
#         courses = Course.objects.order_by("id")
#     except ExternalAPIServiceError as e:
#         error_message = e

    # Pass the API data into the template context dictionary
    # context = {
    #     "assignments": assignments,
    #     "courses": courses,
    #     "error_message": error_message,
    # }

    # return render(request, "assignments.html", context)
        

class AssignmentListView(SingleTableView):
    client = ExternalApiClient()
    error_message = None
    assignments = Assignment.objects.order_by("course_id")
    courses = Course.objects.order_by("id")

    try:
        # Calls the external API service method created earlier
        #assignments = client.fetch_all_assignments()
        if(not Course.objects.exists()):
            client.fetch_all_courses()
        #always check for new assignments
        client.fetch_all_assignments()
        assignments = Assignment.objects.order_by("course_id")
        courses = Course.objects.order_by("id")
    except ExternalAPIServiceError as e:
        error_message = e
    model = Assignment
    table_class = AssignmentTable
    template_name = 'assignments.html'



# class temporary(generic.ListView):
#     template_name = "assignments.html"
#     context_object_name = "course_list"
#     def get(self, request):
#         client = ExternalApiClient()
        
#         # Get requested page number from request query params (?page=2)
#         page = request.GET.get('page', 1)

#         try:
#             paginated_data = client.fetch_all_courses()
            
#             return JsonResponse(paginated_data, status=200)
#         except ExternalAPIServiceError as e:
#             return JsonResponse({"error": str(e)}, status=502)
    
# class ResultsView(generic.ListView):
#     model = Question
#     template_name = "results.html"
    


# def filter_by_course(request, course_id):
#     course = get_object_or_404(Course, pk=course_id)
#     try:
#         selected_course = assignment.filter(pk=request.POST["course"])
#     except (KeyError, Course.DoesNotExist):
#         # display original table.
#         return render(
#             request,
#             "assignment.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse("fullstack:assignments", args=(course.id,)))
    

