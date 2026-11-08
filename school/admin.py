from django.contrib import admin

from .forms import CourseForm
from .models import Classroom, Course, DayOfTheWeek


admin.site.register(DayOfTheWeek)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "school")
    list_filter = ("school",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    list_display = (
        "subject",
        "day_of_the_week",
        "starting_hour",
        "school",
        "classroom",
    )
    list_filter = ("school", "day_of_the_week")

    class Media:
        js = ("js/course-classroom-select.js",)
