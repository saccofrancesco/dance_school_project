from django.db.models import Prefetch
from django.views.generic import DetailView, ListView

from school.models import Classroom, Course

from .models import School


class SchoolDetailView(DetailView):
    model = School
    context_object_name = "school"
    template_name = "schoolmanagement/school_detail.html"
    queryset = School.objects.prefetch_related(
        Prefetch("classrooms", queryset=Classroom.objects.order_by("name")),
        Prefetch(
            "courses",
            queryset=Course.objects.select_related(
                "day_of_the_week", "classroom"
            ).order_by("day_of_the_week__number", "starting_hour", "subject"),
        ),
    )


class SchoolListView(ListView):
    model = School
    context_object_name = "schools"
    template_name = "schoolmanagement/school_list.html"
