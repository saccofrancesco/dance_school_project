from django.urls import path

from .views import (
    ClassroomDetailView,
    ClassroomListView,
    CourseCreateView,
    CourseDeleteView,
    CourseDetailView,
    CourseListView,
    CourseUpdateView,
    classrooms_for_school,
    DayOfTheWeekCreateView,
    DayOfTheWeekDetailView,
    DayOfTheWeekListView,
    DayOfTheWeekUpdateView,
)

urlpatterns = [
    path("days/", DayOfTheWeekListView.as_view(), name="day_of_the_week_list"),
    path(
        "days/<int:pk>/",
        DayOfTheWeekDetailView.as_view(),
        name="day_of_the_week_detail",
    ),
    path("days/new/", DayOfTheWeekCreateView.as_view(), name="day_of_the_week_create"),
    path(
        "days/<int:pk>/edit/",
        DayOfTheWeekUpdateView.as_view(),
        name="day_of_the_week_update",
    ),
    path("classrooms/", ClassroomListView.as_view(), name="classroom_list"),
    path(
        "classrooms/by-school/",
        classrooms_for_school,
        name="classrooms_for_school",
    ),
    path(
        "classrooms/<int:pk>/",
        ClassroomDetailView.as_view(),
        name="classroom_detail",
    ),
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("courses/new/", CourseCreateView.as_view(), name="course_create"),
    path(
        "courses/<int:pk>/edit/",
        CourseUpdateView.as_view(),
        name="course_update",
    ),
    path(
        "courses/<int:pk>/delete/",
        CourseDeleteView.as_view(),
        name="course_delete",
    ),
]
