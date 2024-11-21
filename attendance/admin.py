from django.contrib import admin
from .models import Lesson, Attendance  # Импорт существующих моделей из models.py

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'schedule_time')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'lesson_schedule_time', 'checked_in')

    def lesson_schedule_time(self, obj):
        return obj.lesson.schedule_time

    lesson_schedule_time.short_description = "Дата и время занятия"