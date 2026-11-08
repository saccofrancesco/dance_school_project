from django.urls import path

from .views import (
    ClassroomDetailView,
    ClassroomListView,
    CourseDetailView,
    CourseListView,
    DayOfTheWeekDetailView,
    DayOfTheWeekListView,
)

urlpatterns = [
    path("days/", DayOfTheWeekListView.as_view(), name="day_of_the_week_list"),
    path(
        "days/<int:pk>/",
        DayOfTheWeekDetailView.as_view(),
        name="day_of_the_week_detail",
    ),
    path("classrooms/", ClassroomListView.as_view(), name="classroom_list"),
    path(
        "classrooms/<int:pk>/",
        ClassroomDetailView.as_view(),
        name="classroom_detail",
    ),
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
]
