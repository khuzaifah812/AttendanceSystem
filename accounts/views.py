from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from audit.models import AuditLog

User=get_user_model()
class LoginAPI(APIView):
    authentication_classes=[]
    permission_classes=[]
    def post(self, r):
        username=r.data.get('username')
        password=r.data.get('password')
        user=authenticate(r, username=username, password=password)
        if not user:
            AuditLog.objects.create(user=None, action='FAILED_LOGIN', description=f"Failed login {username}", ip_address=r.META.get('REMOTE_ADDR',''))
            return Response({"error":"Invalid credentials"}, status=400)
        login(r, user)
        AuditLog.objects.create(user=user, action='LOGIN', description=f"{user.username} logged in", ip_address=r.META.get('REMOTE_ADDR',''))
        return Response({"role":user.role, "username":user.username})

class LogoutAPI(APIView):
    def post(self, r):
        logout(r)
        return Response({"message":"Logged out"})

class ProfileAPI(APIView):
    def get(self, r):
        u=r.user
        if u.role=='STUDENT':
            s=u.student_profile
            return Response({"registration_number":s.registration_number,"full_name":s.full_name,"programme":str(s.programme),"year":s.year_of_study})
        elif u.role=='LECTURER':
            l=u.lecturer_profile
            return Response({"staff_number":l.staff_number,"full_name":l.full_name})
        else:
            return Response({"username":u.username,"role":u.role})
        
        from django.contrib.auth.decorators import login_required
from django.db.models import Count


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Lecturer

# Safe imports - will not crash even if model name different
try:
    from attendance.models import AttendanceRecord
except:
    AttendanceRecord = None

try:
    from lectures.models import Lecture
except:
    Lecture = None

try:
    from courses.models import Course
except:
    Course = None

try:
    from programmes.models import Programme
except:
    Programme = None

@login_required
def admin_dashboard(request):
    if not (hasattr(request.user, 'role') and request.user.role == 'ADMIN' or request.user.is_superuser):
        return redirect('/admin/login/')

    context = {
        'total_students': Student.objects.count(),
        'total_lecturers': Lecturer.objects.count(),
        'total_courses': Course.objects.count() if Course else 0,
        'total_lectures': Lecture.objects.count() if Lecture else 0,
        'total_programmes': Programme.objects.count() if Programme else 0,
        'recent_attendance': AttendanceRecord.objects.order_by('-id')[:10] if AttendanceRecord else [],
        'recent_students': Student.objects.order_by('-id')[:5],
    }
    return render(request, 'admin_dashboard.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def custom_login(request):
    # If already logged in, go straight to dashboard
    if request.user.is_authenticated:
        if request.user.is_superuser or getattr(request.user, 'role', '') == 'ADMIN':
            return redirect('/dashboard/')
        elif getattr(request.user, 'role', '') == 'LECTURER':
            return redirect('/lecturer/')
        else:
            return redirect('/student/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser or getattr(user, 'role', '') == 'ADMIN':
                return redirect('/dashboard/')
            elif getattr(user, 'role', '') == 'LECTURER':
                return redirect('/lecturer/')
            else:
                return redirect('/student/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')