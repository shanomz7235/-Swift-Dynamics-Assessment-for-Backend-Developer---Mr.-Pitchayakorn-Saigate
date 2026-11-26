from django.db.models import Count
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apis.filters import SchoolFilter
from apis.models import School
from apis.serializers import SchoolSerializer


class SchoolViewSet(ModelViewSet):
    serializer_class = SchoolSerializer
    filterset_class = SchoolFilter
    permission_classes = [AllowAny]

    def get_queryset(self):
        return School.objects.annotate(
            classroom_count=Count("classrooms", distinct=True),
            teacher_count=Count("classrooms__teachers", distinct=True),
            student_count=Count("classrooms__students", distinct=True),
        ).order_by("id")