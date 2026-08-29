from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .services import get_active_lecture_for_student, create_attendance_record
from .models import Attendance
from audit.models import AuditLog

class ActiveAttendanceAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, r):
        if r.user.role!='STUDENT':
            return Response({"lecture":None})
        student=r.user.student_profile
        lec=get_active_lecture_for_student(student)
        if not lec:
            return Response({"lecture":None, "message":"No attendance session is currently active."})
        already=Attendance.objects.filter(student=student, lecture=lec).exists()
        return Response({"lecture":{
            "id":lec.id,"course_name":lec.course.course_name,"course_code":lec.course.course_code,
            "room":lec.room,"start_time":str(lec.start_time),"end_time":str(lec.end_time),
            "status":lec.status,"already_checked":already
        }})

class CheckInAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, r):
        if r.user.role!='STUDENT':
            return Response({"error":"Only students"}, status=403)
        student=r.user.student_profile
        lecture=get_active_lecture_for_student(student)
        if not lecture:
            return Response({"error":"No attendance session is currently active."}, status=400)
        try:
            lat=float(r.data.get('latitude'))
            lon=float(r.data.get('longitude'))
            acc=float(r.data.get('accuracy',0))
        except:
            return Response({"error":"Invalid GPS"}, status=400)
        try:
            att=create_attendance_record(student, lecture, lat, lon, acc, r.META.get('REMOTE_ADDR','0.0.0.0'), r.META.get('HTTP_USER_AGENT',''))
            AuditLog.objects.create(user=r.user, action='CHECK_IN', description=f"Checked in lecture {lecture.id}", ip_address=r.META.get('REMOTE_ADDR',''))
            return Response({"message":f"Attendance successfully recorded. Check-in time: {att.check_in_time.strftime('%H:%M:%S')}"})
        except ValueError as e:
            AuditLog.objects.create(user=r.user, action='REJECTED_CHECK_IN', description=str(e), ip_address=r.META.get('REMOTE_ADDR',''))
            return Response({"error":str(e)}, status=400)

class StudentHistoryAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, r):
        student=r.user.student_profile
        atts=Attendance.objects.filter(student=student).select_related('lecture__course').order_by('-check_in_time')[:50]
        data=[{"course":a.lecture.course.course_name,"date":str(a.attendance_date),"time":a.check_in_time.strftime("%H:%M:%S"),"status":a.status} for a in atts]
        return Response(data)