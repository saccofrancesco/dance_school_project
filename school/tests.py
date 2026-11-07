from datetime import time

from django.test import TestCase
from django.urls import reverse

from school.models import Classroom, Course, DayOfTheWeek
from schoolmanagement.models import School


class SchoolViewsTests(TestCase):
    def setUp(self):
        self.day = DayOfTheWeek.objects.create(number=1, name="Lunedì")
        self.classroom = Classroom.objects.create(name="Sala A", capacity=20)
        self.school = School.objects.create(
            name="Danza Aurora",
            street="Via Esempio 1",
            city="Milano",
            province="MI",
            zip="20121",
            country="Italia",
            website="https://example.com",
            phone="+39 02 0000 0001",
            email="milano@example.com",
            vat="00000000001",
        )
        self.course = Course.objects.create(
            subject="Danza classica",
            day_of_the_week=self.day,
            starting_hour=time(18, 30),
            classroom=self.classroom,
            school=self.school,
        )

    def test_day_list_and_detail_render(self):
        list_response = self.client.get(reverse("day_of_the_week_list"))
        detail_response = self.client.get(
            reverse("day_of_the_week_detail", kwargs={"pk": self.day.pk})
        )

        self.assertContains(list_response, "Lunedì")
        self.assertContains(detail_response, "Lunedì")
        self.assertContains(detail_response, "1")

    def test_classroom_list_and_detail_render(self):
        list_response = self.client.get(reverse("classroom_list"))
        detail_response = self.client.get(
            reverse("classroom_detail", kwargs={"pk": self.classroom.pk})
        )

        self.assertContains(list_response, "Sala A")
        self.assertContains(list_response, "20")
        self.assertContains(detail_response, "Sala A")
        self.assertContains(detail_response, "20")

    def test_course_list_and_detail_render(self):
        list_response = self.client.get(reverse("course_list"))
        detail_response = self.client.get(
            reverse("course_detail", kwargs={"pk": self.course.pk})
        )

        self.assertContains(list_response, "Danza classica")
        self.assertContains(list_response, "Lunedì")
        self.assertContains(list_response, "18:30")
        self.assertContains(list_response, "Sala A")
        self.assertContains(list_response, "Danza Aurora")
        self.assertContains(detail_response, "Danza classica")
        self.assertContains(detail_response, "18:30")
        self.assertContains(detail_response, "Sala A")
        self.assertContains(detail_response, "Danza Aurora")

    def test_detail_views_return_404_for_missing_objects(self):
        detail_routes = (
            "day_of_the_week_detail",
            "classroom_detail",
            "course_detail",
        )
        for route_name in detail_routes:
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name, kwargs={"pk": 99999}))
                self.assertEqual(response.status_code, 404)

    def test_deleting_day_deletes_related_course(self):
        self.day.delete()

        self.assertFalse(Course.objects.filter(pk=self.course.pk).exists())

    def test_deleting_classroom_deletes_related_course(self):
        self.classroom.delete()

        self.assertFalse(Course.objects.filter(pk=self.course.pk).exists())

    def test_deleting_school_deletes_related_course(self):
        self.school.delete()

        self.assertFalse(Course.objects.filter(pk=self.course.pk).exists())
