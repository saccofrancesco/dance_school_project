from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
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
