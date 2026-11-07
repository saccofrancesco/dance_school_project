from django.views.generic import DetailView, ListView

from .models import Classroom, Course, DayOfTheWeek


class DayOfTheWeekListView(ListView):
    model = DayOfTheWeek
    context_object_name = "days"
    template_name = "school/day_of_the_week_list.html"


class DayOfTheWeekDetailView(DetailView):
    model = DayOfTheWeek
    context_object_name = "day"
    template_name = "school/day_of_the_week_detail.html"


class ClassroomListView(ListView):
    model = Classroom
    context_object_name = "classrooms"
    template_name = "school/classroom_list.html"


class ClassroomDetailView(DetailView):
    model = Classroom
    context_object_name = "classroom"
    template_name = "school/classroom_detail.html"


class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    queryset = Course.objects.select_related(
        "day_of_the_week", "classroom", "school"
    )
    template_name = "school/course_list.html"


class CourseDetailView(DetailView):
    model = Course
    context_object_name = "course"
    queryset = Course.objects.select_related(
        "day_of_the_week", "classroom", "school"
    )
    template_name = "school/course_detail.html"
