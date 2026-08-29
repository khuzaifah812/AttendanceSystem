import math
from django.utils import timezone
from django.db import transaction
from campus.models import CampusConfiguration
from courses.models import Enrollment
from .models import Attendance

def calculate_distance(lat1, lon1, lat2, lon2):
    R=6371000
    phi1,phi2=math.radians(lat1),math.radians(lat2)
    dphi=math.radians(lat2-lat1)
    dlambda=math.radians(lon2-lon1)
    a=math.sin(dphi/2)**2+math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R*2*math.atan2(math.sqrt(a), math.sqrt(1-a))

def get_active_lecture_for_student(student):
    now=timezone.now()
    active=Attendance._meta.get_field('lecture').related_model.objects.filter(
        status='ATTENDANCE_ACTIVE',
        attendance_start_time__lte=now,
        attendance_end_time__gte=now
    )
    # Filter to courses student enrolled
    enrolled_courses=Enrollment.objects.filter(student=student).values_list('course_id', flat=True)
    return active.filter(course_id__in=enrolled_courses).first()

@transaction.atomic
def create_attendance_record(student, lecture, lat, lon, accuracy, ip, ua):
    if Attendance.objects.filter(student=student, lecture=lecture).exists():
        raise ValueError("You have already checked in for this lecture.")
    campus=CampusConfiguration.objects.filter(status='ACTIVE').first()
    if not campus:
        raise ValueError("Campus not configured")
    dist=calculate_distance(float(lat), float(lon), float(campus.latitude), float(campus.longitude))
    if dist > campus.allowed_radius_meters:
        raise ValueError("You are outside the school campus. Attendance cannot be recorded.")
    if lecture.status!='ATTENDANCE_ACTIVE':
        raise ValueError("Attendance is not active")
    if timezone.now() > lecture.attendance_end_time:
        raise ValueError("Attendance deadline passed")
    if not Enrollment.objects.filter(student=student, course=lecture.course).exists():
        raise ValueError("You are not enrolled in this course")
    return Attendance.objects.create(
        student=student, lecture=lecture, latitude=lat, longitude=lon,
        gps_accuracy=accuracy, distance_from_campus=dist,
        location_verified=True, ip_address=ip, user_agent=ua, status='PRESENT'
    )