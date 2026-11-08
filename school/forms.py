from django import forms
from django.urls import reverse

from .models import Classroom, Course


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("day_of_the_week", "classroom", "school"):
            self.fields[field_name].empty_label = "Seleziona un’opzione"

        school_id = self.data.get(self.add_prefix("school")) if self.is_bound else None
        if school_id is None and self.instance.pk:
            school_id = self.instance.school_id

        classroom_field = self.fields["classroom"]
        classroom_field.queryset = classroom_field.queryset.none()
        classroom_field.help_text = "Scegli prima una sede per visualizzare le sue aule."
        classroom_field.widget.attrs["disabled"] = True
        classroom_field.widget.attrs["data-classrooms-url"] = reverse(
            "classrooms_for_school"
        )
        classroom_field.widget.attrs["data-placeholder"] = "Seleziona un’aula"
        self.fields["school"].widget.attrs["data-classrooms-url"] = reverse(
            "classrooms_for_school"
        )

        if school_id and str(school_id).isdecimal():
            classroom_field.queryset = Classroom.objects.filter(
                school_id=school_id
            ).order_by("name")

    class Meta:
        model = Course
        fields = [
            "subject",
            "day_of_the_week",
            "school",
            "classroom",
            "starting_hour",
        ]
        widgets = {
            "starting_hour": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
        }
