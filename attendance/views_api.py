from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Lesson, Attendance
from .serializers import LessonSerializer, AttendanceSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]