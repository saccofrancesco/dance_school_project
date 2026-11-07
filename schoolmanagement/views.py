from django.views.generic import DetailView, ListView

from .models import School


class SchoolDetailView(DetailView):
    model = School
    context_object_name = "school"
    template_name = "schoolmanagement/school_detail.html"


class SchoolListView(ListView):
    model = School
    context_object_name = "schools"
    template_name = "schoolmanagement/school_list.html"
