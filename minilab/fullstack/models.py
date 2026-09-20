from django.db import models
import datetime
from django.utils import timezone

class Course(models.Model):
    name = models.CharField(max_length=200)
    id = models.CharField(max_length=200, primary_key = True)
    date_created = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Assignment(models.Model):
    name = models.CharField(max_length=200)
    due_date = models.CharField(max_length=200)
    html_url = models.CharField(max_length=200)
    #python says this is a nonnullable value. why?
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    submitted = False
    def __str__(self):
        return self.name
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)



