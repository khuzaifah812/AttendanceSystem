from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.generic import TemplateView
from accounts.views import admin_dashboard, custom_login

def health(r): return JsonResponse({"status":"ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health),
    path('api/auth/', include('accounts.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('attendance.urls')),
    path('api/', include('lectures.urls')),
    path('api/admin/', include('programmes.urls')),
    path('accounts/', include('accounts.urls')),
    path('manage/', include('manage.urls')),  # <-- ADD THIS LINE
    path('', include('accounts.urls')),
    path('', custom_login, name='home'),
    path('student/', TemplateView.as_view(template_name='student_dashboard.html')),
    path('lecturer/', TemplateView.as_view(template_name='lecturer_dashboard.html')),
    path('dashboard/', admin_dashboard, name='dashboard'),
]
