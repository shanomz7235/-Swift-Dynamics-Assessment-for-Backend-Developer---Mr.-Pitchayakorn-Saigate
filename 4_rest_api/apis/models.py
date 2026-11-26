from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return self.name


class Classroom(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="classrooms",
    )
    grade = models.PositiveSmallIntegerField()
    section = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["school_id", "grade", "section"]
        constraints = [
            models.UniqueConstraint(
                fields=["school", "grade", "section"],
                name="unique_classroom_per_school",
            )
        ]

    def __str__(self):
        return f"{self.grade}/{self.section} - {self.school}"


class Teacher(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    classrooms = models.ManyToManyField(
        Classroom,
        related_name="teachers",
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name="students",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
