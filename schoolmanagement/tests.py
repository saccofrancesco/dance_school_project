from django.test import TestCase
from django.urls import reverse

from .models import School


class SchoolViewsTests(TestCase):
    def setUp(self):
        self.school = self.create_school()

    def create_school(self, **overrides):
        school_data = {
            "name": "Dance School Milano",
            "street": "Via Esempio 1",
            "city": "Milano",
            "province": "MI",
            "zip": "20121",
            "country": "Italia",
            "website": "https://example.com",
            "phone": "+39 02 0000 0001",
            "email": "milano@example.com",
            "vat": "00000000001",
        }
        school_data.update(overrides)
        return School.objects.create(**school_data)

    def test_school_list_displays_entries_and_detail_links(self):
        second_school = self.create_school(
            name="Dance School Monza",
            street="Via Esempio 2",
            phone="+39 039 0000 0002",
            email="monza@example.com",
        )

        response = self.client.get(reverse("school_list"))

        self.assertContains(response, self.school.name)
        self.assertContains(response, self.school.street)
        self.assertContains(response, self.school.phone)
        self.assertContains(response, self.school.email)
        self.assertContains(response, second_school.name)
        self.assertContains(
            response,
            reverse("school_detail", kwargs={"pk": self.school.pk}),
        )
        self.assertContains(
            response,
            reverse("school_detail", kwargs={"pk": second_school.pk}),
        )

    def test_school_list_shows_empty_state(self):
        School.objects.all().delete()

        response = self.client.get(reverse("school_list"))

        self.assertContains(response, "Nessuna sede disponibile.")

    def test_school_detail_displays_all_school_information(self):
        response = self.client.get(
            reverse("school_detail", kwargs={"pk": self.school.pk})
        )

        self.assertContains(response, self.school.name)
        self.assertContains(response, self.school.street)
        self.assertContains(response, self.school.city)
        self.assertContains(response, self.school.province)
        self.assertContains(response, self.school.zip)
        self.assertContains(response, self.school.country)
        self.assertContains(response, self.school.website)
        self.assertContains(response, self.school.phone)
        self.assertContains(response, self.school.email)
        self.assertContains(response, self.school.vat)
        self.assertEqual(response.context["school"], self.school)

    def test_school_detail_returns_404_for_missing_school(self):
        response = self.client.get(reverse("school_detail", kwargs={"pk": 99999}))

        self.assertEqual(response.status_code, 404)

    def test_school_string_representation_is_its_name(self):
        self.assertEqual(str(self.school), self.school.name)
