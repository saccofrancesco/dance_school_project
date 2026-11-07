from django.contrib import admin
from .models import Classroom, Course, DayOfTheWeek

admin.site.register([DayOfTheWeek, Classroom, Course])
