from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Lecture
from attendance.models import Attendance
from courses.models import Enrollment
from accounts.permissions import IsLecturer, IsAdmin
from audit.models import AuditLog

class LecturerLecturesAPI(APIView):
    permission_classes=[IsAuthenticated, IsLecturer]
    def get(self, r):
        lectures=Lecture.objects.filter(lecturer__user=r.user, lecture_date=timezone.now().date()).order_by('start_time')
        data=[]
        for lec in lectures:
            present=Attendance.objects.filter(lecture=lec).count()
            expected=Enrollment.objects.filter(course=lec.course).count()
            data.append({
                "id":lec.id,"course":lec.course.course_name,"course_code":lec.course.course_code,
                "room":lec.room,"start_time":str(lec.start_time),"end_time":str(lec.end_time),
                "status":lec.status,"expected":expected,"present":present,"absent":expected-present
            })
        return Response(data)

class StartAttendanceAPI(APIView):
    permission_classes=[IsAuthenticated, IsLecturer]
    def post(self, r, id):
        try:
            lec=Lecture.objects.get(id=id, lecturer__user=r.user)
        except Lecture.DoesNotExist:
            return Response({"error":"Not your lecture"}, status=403)
        lec.status='ATTENDANCE_ACTIVE'
        lec.attendance_start_time=timezone.now()
        lec.attendance_end_time=timezone.now()+timezone.timedelta(minutes=20)
        lec.save()
        AuditLog.objects.create(user=r.user, action='ATTENDANCE_STARTED', description=f"Started attendance for lecture {lec.id}", ip_address=r.META.get('REMOTE_ADDR',''))
        return Response({"status":"ATTENDANCE_ACTIVE","end":lec.attendance_end_time})

class EndAttendanceAPI(APIView):
    permission_classes=[IsAuthenticated, IsLecturer]
    def post(self, r, id):
        lec=Lecture.objects.get(id=id, lecturer__user=r.user)
        lec.status='ATTENDANCE_CLOSED'
        lec.save()
        AuditLog.objects.create(user=r.user, action='ATTENDANCE_ENDED', description=f"Ended attendance for lecture {lec.id}", ip_address=r.META.get('REMOTE_ADDR',''))
        return Response({"status":"ATTENDANCE_CLOSED"})

class LectureAttendanceListAPI(APIView):
    permission_classes=[IsAuthenticated, IsLecturer]
    def get(self, r, id):
        lec=Lecture.objects.get(id=id, lecturer__user=r.user)
        atts=Attendance.objects.filter(lecture=lec).select_related('student').order_by('check_in_time')
        data=[{"registration_number":a.student.registration_number,"full_name":a.student.full_name,"check_in_time":a.check_in_time.strftime("%H:%M:%S"),"status":a.status} for a in atts]
        return Response(data)