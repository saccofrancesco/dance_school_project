from django.urls import path

from .views import SchoolDetailView, SchoolListView

urlpatterns = [
    path("", SchoolListView.as_view(), name="school_list"),
    path("<int:pk>/", SchoolDetailView.as_view(), name="school_detail"),
]
