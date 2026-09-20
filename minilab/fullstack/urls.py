from django.urls import path
from . import views

app_name = "fullstack"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("assignments", views.AssignmentListView.as_view(), name="assignments"),
    #path("<int:question_id>/vote/", views.vote, name="vote"),
]