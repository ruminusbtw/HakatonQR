from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views_api import LessonViewSet, AttendanceViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/<int:lesson_id>/qrcode/', views.qr_code_page, name='qr_code_page'),
    # path('lessons/<int:lesson_id>/generate_qr/', views.generate_qr_view, name='generate_qr'),
    path('lessons/<int:lesson_id>/confirm/<str:qr_hash>/', views.confirm_attendance_view, name='confirm_attendance'),
]
urlpatterns += router.urls

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]