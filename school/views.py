from django.urls import reverse_lazy
from django.views import generic

from .forms import CourseForm
from .models import Classroom, Course, DayOfTheWeek


class DayOfTheWeekListView(generic.ListView):
    model = DayOfTheWeek
    context_object_name = "days"
    template_name = "school/day_of_the_week_list.html"


class DayOfTheWeekDetailView(generic.DetailView):
    model = DayOfTheWeek
    context_object_name = "day"
    template_name = "school/day_of_the_week_detail.html"


class DayOfTheWeekCreateView(generic.CreateView):
    model = DayOfTheWeek
    fields = ["name", "number"]
    template_name = "school/day_of_the_week_form.html"
    success_url = reverse_lazy("day_of_the_week_list")


class DayOfTheWeekUpdateView(generic.UpdateView):
    model = DayOfTheWeek
    fields = ["name", "number"]
    template_name = "school/day_of_the_week_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "day_of_the_week_detail",
            kwargs={"pk": self.object.pk},
        )


class ClassroomListView(generic.ListView):
    model = Classroom
    context_object_name = "classrooms"
    template_name = "school/classroom_list.html"


class ClassroomDetailView(generic.DetailView):
    model = Classroom
    context_object_name = "classroom"
    template_name = "school/classroom_detail.html"


class CourseListView(generic.ListView):
    model = Course
    context_object_name = "courses"
    queryset = Course.objects.select_related("day_of_the_week", "classroom", "school")
    template_name = "school/course_list.html"


class CourseDetailView(generic.DetailView):
    model = Course
    context_object_name = "course"
    queryset = Course.objects.select_related("day_of_the_week", "classroom", "school")
    template_name = "school/course_detail.html"


class CourseCreateView(generic.CreateView):
    model = Course
    form_class = CourseForm
    template_name = "school/course_form.html"
    success_url = reverse_lazy("course_list")


class CourseUpdateView(generic.UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "school/course_form.html"

    def get_success_url(self):
        return reverse_lazy("course_detail", kwargs={"pk": self.object.pk})


class CourseDeleteView(generic.DeleteView):
    model = Course
    template_name = "school/course_confirm_delete.html"
    success_url = reverse_lazy("course_list")
