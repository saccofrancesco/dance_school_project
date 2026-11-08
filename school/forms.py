from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("day_of_the_week", "classroom", "school"):
            self.fields[field_name].empty_label = "Seleziona un’opzione"

    class Meta:
        model = Course
        fields = [
            "subject",
            "starting_hour",
            "day_of_the_week",
            "classroom",
            "school",
        ]
        widgets = {
            "starting_hour": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
        }
