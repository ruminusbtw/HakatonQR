from io import BytesIO
import base64
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Lesson, Attendance
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
import qrcode
from django.http import JsonResponse
from .utils import generate_qr_code
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def generate_qr_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    qr_hash = lesson.generate_qr_hash()
    confirm_url = f"https://{request.get_host()}{reverse('confirm_attendance', args=[lesson_id, qr_hash])}"
    qr_code = generate_qr_code(confirm_url)

    response = HttpResponse(content_type="image/png")
    response.write(qr_code.read())
    return response

@csrf_exempt
@login_required
def confirm_attendance_view(request, lesson_id, qr_hash):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    expected_hash = lesson.generate_qr_hash()

    if qr_hash != expected_hash:
        return JsonResponse({"success": False, "message": "Неверный или устаревший QR-код!"}, status=400)

    if request.method == "POST":
        attendance, created = Attendance.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            defaults={"checked_in": True, "qr_hash": qr_hash, "checked_in_time": now()}
        )

        if not created:
            attendance.checked_in = True
            attendance.checked_in_time = now()
            attendance.qr_hash = qr_hash
            attendance.save()

        return JsonResponse({"success": True, "message": "Посещение успешно обновлено!"})

    return render(request, 'attendance/confirm_attendance.html', {'lesson': lesson})

@csrf_exempt
@login_required
def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'attendance/lesson_list.html', {'lessons': lessons})

def attendance_view(request):
    attendances = Attendance.objects.all()
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

@csrf_exempt
@login_required
def qr_code_page(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    qr_hash = lesson.generate_qr_hash()
    confirm_url = f"https://{request.get_host()}{reverse('confirm_attendance', args=[lesson_id, qr_hash])}"

    qr_code = qrcode.make(confirm_url)
    buffer = BytesIO()
    qr_code.save(buffer, format="PNG")
    buffer.seek(0)

    qr_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render(request, 'attendance/qr_code.html', {
        'lesson': lesson,
        'qr_image': qr_image,
        'confirm_url': confirm_url,
    })
