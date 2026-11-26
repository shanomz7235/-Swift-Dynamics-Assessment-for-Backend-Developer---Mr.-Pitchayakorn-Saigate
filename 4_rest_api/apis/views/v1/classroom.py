from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apis.filters import ClassroomFilter
from apis.models import Classroom
from apis.serializers import ClassroomDetailSerializer, ClassroomSerializer


class ClassroomViewSet(ModelViewSet):
    queryset = Classroom.objects.all()
    filterset_class = ClassroomFilter
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Classroom.objects.select_related("school").prefetch_related(
            "teachers",
            "students",
        ).order_by("id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ClassroomDetailSerializer
        return ClassroomSerializer
