from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import JsonResponse

def health(r): return JsonResponse({"status":"ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health),
    path('api/auth/', include('accounts.urls')),
    path('accounts/', include('attendance_system.urls')),
    path('api/', include('attendance.urls')),
    path('api/', include('lectures.urls')),
    path('api/admin/', include('programmes.urls')),
    path('', TemplateView.as_view(template_name='login.html'), name='home'),
    path('student/', TemplateView.as_view(template_name='student_dashboard.html')),
    path('lecturer/', TemplateView.as_view(template_name='lecturer_dashboard.html')),
    path('dashboard/', TemplateView.as_view(template_name='admin_dashboard.html')),
]