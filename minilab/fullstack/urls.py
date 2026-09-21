from django.urls import path
from . import views

app_name = "fullstack"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("assignments", views.FilteredAssignmentListView.as_view(), name="filteredassignments"),
]