from rest_framework import serializers
from .models import Classroom, School, Student, Teacher


class SchoolSerializer(serializers.ModelSerializer):
    classroom_count = serializers.SerializerMethodField()
    teacher_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = [
            "id",
            "name",
            "abbreviation",
            "address",
            "classroom_count",
            "teacher_count",
            "student_count",
        ]
        read_only_fields = ["id", "classroom_count", "teacher_count", "student_count"]

    def get_classroom_count(self, school):
        if hasattr(school, "classroom_count"):
            return school.classroom_count
        return school.classrooms.count()

    def get_teacher_count(self, school):
        if hasattr(school, "teacher_count"):
            return school.teacher_count
        return Teacher.objects.filter(classrooms__school=school).distinct().count()

    def get_student_count(self, school):
        if hasattr(school, "student_count"):
            return school.student_count
        return Student.objects.filter(classroom__school=school).count()


class TeacherSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "first_name", "last_name", "gender"]


class StudentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "gender"]


class ClassroomSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ["id", "school", "grade", "section"]


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ["id", "school", "grade", "section"]
        read_only_fields = ["id"]


class ClassroomDetailSerializer(ClassroomSerializer):
    teachers = TeacherSummarySerializer(many=True, read_only=True)
    students = StudentSummarySerializer(many=True, read_only=True)

    class Meta(ClassroomSerializer.Meta):
        fields = ClassroomSerializer.Meta.fields + ["teachers", "students"]


class TeacherSerializer(serializers.ModelSerializer):
    classrooms = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Classroom.objects.all(),
        required=False,
    )

    class Meta:
        model = Teacher
        fields = ["id", "first_name", "last_name", "gender", "classrooms"]
        read_only_fields = ["id"]

    def validate_classrooms(self, classrooms):
        school_ids = {classroom.school_id for classroom in classrooms}
        if len(school_ids) > 1:
            raise serializers.ValidationError(
                "A teacher's classrooms must belong to the same school."
            )
        return classrooms


class TeacherDetailSerializer(TeacherSummarySerializer):
    classrooms = ClassroomSummarySerializer(many=True, read_only=True)

    class Meta(TeacherSummarySerializer.Meta):
        fields = TeacherSummarySerializer.Meta.fields + ["classrooms"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "gender", "classroom"]
        read_only_fields = ["id"]


class StudentDetailSerializer(StudentSummarySerializer):
    classroom = ClassroomSummarySerializer(read_only=True)

    class Meta(StudentSummarySerializer.Meta):
        fields = StudentSummarySerializer.Meta.fields + ["classroom"]
