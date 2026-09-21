from .models import Assignment
from django_filters import FilterSet

class AssignmentFilter(FilterSet):
    class Meta:
        model = Assignment
        fields = {"course": ["exact"]}