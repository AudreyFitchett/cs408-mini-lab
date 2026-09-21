from django import forms
from .models import Assignment

class CourseFilter(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["course"]