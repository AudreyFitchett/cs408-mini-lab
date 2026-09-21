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
from django_filters import FilterSet


class AssignmentFilter(FilterSet):
    class Meta:
        model = Assignment
        fields = {"course": ["exact"]}