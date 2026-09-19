from django.db import models
import datetime
from django.utils import timezone

class Assignment(models.Model):
    name = models.CharField(max_length=200)
    course_id = models.CharField(max_length=200)
    due_date = models.CharField(max_length=200)
    html_url = models.CharField(max_length=200)
    submitted = False
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Course(models.Model):
    name = models.CharField(max_length=200)
    id = models.CharField(max_length=200)
    date_created = models.CharField(max_length=200)
    html_url = models.CharField(max_length=200)
