from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apis.filters import TeacherFilter
from apis.models import Teacher
from apis.serializers import TeacherDetailSerializer, TeacherSerializer


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    filterset_class = TeacherFilter
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Teacher.objects.prefetch_related("classrooms").order_by("id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TeacherDetailSerializer
        return TeacherSerializer