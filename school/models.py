from django.db import models


class DayOfTheWeek(models.Model):
    number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Course(models.Model):
    subject = models.CharField(max_length=150)
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
        return self.subject
