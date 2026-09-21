
from .models import Assignment
import django_tables2 as tables


class AssignmentTable(tables.Table):
    class Meta:
        model = Assignment
        template_name = "django_tables2/bootstrap.html"
        fields = ("course","name", "due_date", "submission")


    