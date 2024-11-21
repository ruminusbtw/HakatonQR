from django.db import models
import hashlib
from django.contrib.auth.models import User
from django.utils.timezone import localtime

class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название занятия")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    schedule_time = models.DateTimeField(verbose_name="Время занятия")

    def __str__(self):
        return self.name

    def generate_qr_hash(self):
        current_time = localtime()

        minute = current_time.minute
        second = current_time.second
        rounded_minute = minute
        rounded_second = 30 if second >= 30 else 0

        data = f"{self.name}:{self.schedule_time}:{current_time.strftime('%Y-%m-%d %H')}:{rounded_minute}:{rounded_second}"

        return hashlib.sha256(data.encode()).hexdigest()

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, verbose_name="Занятие")
    checked_in = models.BooleanField(default=False, verbose_name="Посетил")
    qr_hash = models.CharField(max_length=8, verbose_name="QR Хэш", null=True, blank=True)  # Хэш ограничен 8 символами
    checked_in_time = models.DateTimeField(null=True, blank=True, verbose_name="Время отметки")

    def __str__(self):
        return f"{self.user.username} - {self.lesson.name}"

    def save(self, *args, **kwargs):
        if not self.qr_hash:
            data = f"{self.user.id}:{self.lesson.id}"
            full_hash = hashlib.sha256(data.encode()).hexdigest()
            self.qr_hash = full_hash[:8]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Отметка"
        verbose_name_plural = "Отметки"