
from .models import Assignment, Course
from django.views import generic
from .services import ExternalApiClient, ExternalAPIServiceError
from .tables import AssignmentTable
from .filters import AssignmentFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

#landing page just for fun
class IndexView(generic.ListView):
    template_name = "index.html"

    def get_queryset(self):
        """Return the last five published questions."""
        return Assignment.objects.order_by("course_id")

#Lists all assignments in a table format with a filter button
class FilteredAssignmentListView(SingleTableMixin, FilterView):
    client = ExternalApiClient()
    error_message = None
    assignments = Assignment.objects.order_by("course_id")
    courses = Course.objects.order_by("id")

    try:
        if(not Course.objects.exists()):
            client.fetch_all_courses()

        #always check for new assignments - could maybe edit this by recency
        client.fetch_all_assignments()
        assignments = Assignment.objects.order_by("course_id")
        courses = Course.objects.order_by("id")
    except ExternalAPIServiceError as e:
        error_message = e

    model = Assignment
    table_class = AssignmentTable
    template_name = 'assignments.html'
    filterset_class = AssignmentFilter
    

