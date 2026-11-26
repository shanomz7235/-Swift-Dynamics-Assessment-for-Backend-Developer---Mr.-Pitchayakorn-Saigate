from django.test import TestCase
from rest_framework.test import APIClient

from .models import Classroom, School, Student, Teacher


class SchoolApiTests(TestCase):
    def setUp(self):
        self.client = APIClient(HTTP_ACCEPT="application/json")
        self.school = School.objects.create(
            name="Example School",
            abbreviation="EX",
            address="Bangkok",
        )
        self.classroom = Classroom.objects.create(
            school=self.school,
            grade=4,
            section=1,
        )
        self.teacher = Teacher.objects.create(
            first_name="Somchai",
            last_name="Teacher",
            gender=Teacher.Gender.MALE,
        )
        self.teacher.classrooms.add(self.classroom)
        self.student = Student.objects.create(
            first_name="Suda",
            last_name="Student",
            gender=Student.Gender.FEMALE,
            classroom=self.classroom,
        )

    def test_school_detail_includes_related_counts(self):
        response = self.client.get(f"/api/v1/schools/{self.school.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["classroom_count"], 1)
        self.assertEqual(response.data["teacher_count"], 1)
        self.assertEqual(response.data["student_count"], 1)

    def test_school_list_filters_by_partial_name(self):
        response = self.client.get("/api/v1/schools/?name=example")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.school.pk)

    def test_school_can_be_created_updated_and_deleted(self):
        create_response = self.client.post(
            "/api/v1/schools/",
            {
                "name": "Temporary School",
                "abbreviation": "TMP",
                "address": "Chiang Mai",
            },
            format="json",
        )
        school_id = create_response.data["id"]

        self.assertEqual(create_response.status_code, 201)
        update_response = self.client.patch(
            f"/api/v1/schools/{school_id}/",
            {"name": "Updated School"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data["name"], "Updated School")

        delete_response = self.client.delete(f"/api/v1/schools/{school_id}/")
        self.assertEqual(delete_response.status_code, 204)

    def test_classroom_detail_includes_teachers_and_students(self):
        response = self.client.get(f"/api/v1/classrooms/{self.classroom.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["teachers"][0]["id"], self.teacher.pk)
        self.assertEqual(response.data["students"][0]["id"], self.student.pk)

    def test_classroom_list_filters_by_school(self):
        response = self.client.get(
            f"/api/v1/classrooms/?school={self.school.pk}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.classroom.pk)

    def test_teacher_create_and_filter_by_school(self):
        create_response = self.client.post(
            "/api/v1/teachers/",
            {
                "first_name": "Another",
                "last_name": "Teacher",
                "gender": Teacher.Gender.OTHER,
                "classrooms": [self.classroom.pk],
            },
            format="json",
        )

        self.assertEqual(create_response.status_code, 201)
        list_response = self.client.get(
            f"/api/v1/teachers/?school={self.school.pk}&firstname=another"
        )
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data), 1)

    def test_teacher_cannot_be_assigned_to_classrooms_from_different_schools(self):
        other_school = School.objects.create(
            name="Other School",
            abbreviation="OS",
            address="Chiang Mai",
        )
        other_classroom = Classroom.objects.create(
            school=other_school,
            grade=5,
            section=3,
        )

        response = self.client.post(
            "/api/v1/teachers/",
            {
                "first_name": "Cross",
                "last_name": "School",
                "gender": Teacher.Gender.OTHER,
                "classrooms": [self.classroom.pk, other_classroom.pk],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("classrooms", response.data)

    def test_student_detail_includes_classroom(self):
        response = self.client.get(f"/api/v1/students/{self.student.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["classroom"]["id"], self.classroom.pk)

    def test_student_list_filters_by_classroom(self):
        response = self.client.get(
            f"/api/v1/students/?classroom={self.classroom.pk}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.student.pk)
