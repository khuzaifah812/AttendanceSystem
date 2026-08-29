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