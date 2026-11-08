from datetime import time

from django.core.exceptions import ValidationError
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
            zip_code="20121",
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

    def test_classroom_detail_lists_related_courses(self):
        response = self.client.get(
            reverse("classroom_detail", kwargs={"pk": self.classroom.pk})
        )

        self.assertContains(response, self.course.subject)
        self.assertContains(
            response,
            reverse("course_detail", kwargs={"pk": self.course.pk}),
        )

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

    def test_day_can_be_created_and_updated_without_signing_in(self):
        create_response = self.client.post(
            reverse("day_of_the_week_create"),
            {"name": "Martedì", "number": "2"},
        )
        created_day = DayOfTheWeek.objects.get(name="Martedì")
        self.assertRedirects(create_response, reverse("day_of_the_week_list"))

        update_response = self.client.post(
            reverse("day_of_the_week_update", kwargs={"pk": created_day.pk}),
            {"name": "Mercoledì", "number": "3"},
        )

        created_day.refresh_from_db()
        self.assertRedirects(
            update_response,
            reverse("day_of_the_week_detail", kwargs={"pk": created_day.pk}),
        )
        self.assertEqual(created_day.name, "Mercoledì")
        self.assertEqual(created_day.number, 3)

    def test_day_form_shows_validation_errors(self):
        response = self.client.post(
            reverse("day_of_the_week_create"),
            {"name": "", "number": "non è un numero"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(DayOfTheWeek.objects.count(), 1)

    def test_course_can_be_created_with_minute_precision(self):
        response = self.client.post(
            reverse("course_create"),
            {
                "subject": "Danza moderna",
                "starting_hour": "19:15",
                "day_of_the_week": self.day.pk,
                "classroom": self.classroom.pk,
                "school": self.school.pk,
            },
        )

        created_course = Course.objects.get(subject="Danza moderna")
        self.assertRedirects(response, reverse("course_list"))
        self.assertEqual(created_course.starting_hour, time(19, 15))

    def test_invalid_course_time_is_rejected(self):
        response = self.client.post(
            reverse("course_create"),
            {
                "subject": "Danza moderna",
                "starting_hour": "non è un orario",
                "day_of_the_week": self.day.pk,
                "classroom": self.classroom.pk,
                "school": self.school.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Course.objects.count(), 1)

    def test_course_can_be_updated_without_signing_in(self):
        response = self.client.post(
            reverse("course_update", kwargs={"pk": self.course.pk}),
            {
                "subject": "Danza contemporanea",
                "starting_hour": "20:45",
                "day_of_the_week": self.day.pk,
                "classroom": self.classroom.pk,
                "school": self.school.pk,
            },
        )

        self.course.refresh_from_db()
        self.assertRedirects(
            response,
            reverse("course_detail", kwargs={"pk": self.course.pk}),
        )
        self.assertEqual(self.course.subject, "Danza contemporanea")
        self.assertEqual(self.course.starting_hour, time(20, 45))

    def test_course_delete_requires_confirmation_then_deletes(self):
        delete_url = reverse("course_delete", kwargs={"pk": self.course.pk})
        confirmation_response = self.client.get(delete_url)

        self.assertEqual(confirmation_response.status_code, 200)
        self.assertContains(confirmation_response, self.course.subject)
        self.assertTrue(Course.objects.filter(pk=self.course.pk).exists())

        delete_response = self.client.post(delete_url)

        self.assertRedirects(delete_response, reverse("course_list"))
        self.assertFalse(Course.objects.filter(pk=self.course.pk).exists())

    def test_course_form_rejects_subject_longer_than_100_characters(self):
        response = self.client.post(
            reverse("course_create"),
            {
                "subject": "x" * 101,
                "starting_hour": "19:15",
                "day_of_the_week": self.day.pk,
                "classroom": self.classroom.pk,
                "school": self.school.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("subject", response.context["form"].errors)
        self.assertEqual(Course.objects.count(), 1)
