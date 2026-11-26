from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apis.filters import StudentFilter
from apis.models import Student
from apis.serializers import StudentDetailSerializer, StudentSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    filterset_class = StudentFilter
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Student.objects.select_related("classroom").order_by("id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StudentDetailSerializer
        return StudentSerializer