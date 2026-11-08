from django.core.exceptions import ValidationError
from django.db import models


class DayOfTheWeek(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    school = models.ForeignKey(
        "schoolmanagement.School",
        on_delete=models.CASCADE,
        related_name="classrooms",
    )

    def __str__(self):
        return f"{self.name} ({self.capacity} posti)"


class Course(models.Model):
    subject = models.CharField(max_length=100)
    day_of_the_week = models.ForeignKey(
        DayOfTheWeek,
        on_delete=models.CASCADE,
        related_name="courses",
    )
    starting_hour = models.TimeField()
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name="courses",
    )
    school = models.ForeignKey(
        "schoolmanagement.School",
        on_delete=models.CASCADE,
        related_name="courses",
    )

    def __str__(self):
        return f"{self.subject} ({self.day_of_the_week} alle {self.starting_hour:%H:%M})"

    def clean(self):
        super().clean()
        if (
            self.school_id
            and self.classroom_id
            and Classroom.objects.filter(pk=self.classroom_id)
            .exclude(school_id=self.school_id)
            .exists()
        ):
            raise ValidationError(
                {"classroom": "Seleziona un’aula appartenente alla sede scelta."}
            )
