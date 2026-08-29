from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Student, Lecturer
from programmes.models import Programme
from courses.models import Course, Enrollment
from campus.models import CampusConfiguration
from lectures.models import Lecture
from datetime import date, time, timedelta
from django.utils import timezone

User=get_user_model()
class Command(BaseCommand):
    def handle(self, *args, **options):
        prog, _ = Programme.objects.get_or_create(name="Diploma in Software Engineering", code="DSWE")
        campus, _ = CampusConfiguration.objects.get_or_create(school_name="UICT", defaults={"latitude":0.3476, "longitude":32.5825, "allowed_radius_meters":900})
        
        if not User.objects.filter(username='admin').exists():
            u=User.objects.create_user(username='admin', password='admin123', role='ADMIN', is_staff=True, is_superuser=True)
        
        for i in range(1,7):
            uname=f"LEC00{i}"
            if not User.objects.filter(username=uname).exists():
                u=User.objects.create_user(username=uname, password='Lecturer123', role='LECTURER')
                Lecturer.objects.create(user=u, staff_number=f"STAFF/00{i}", first_name=f"Lecturer{i}", last_name="UICT", email=f"lec{i}@uict.ac.ug", department="Computing")

        courses=[]
        for code,name in [("SWE1201","Working with Data"),("SWE1202","Software Testing"),("SWE1203","ICT PROJECT MANAGEMENT"),("SWE1204","Foundation of UI/UX Design"),("SWE1205","Mobile Application Development"),("SWE1206","Cyber Security and Data Privancy"),("SWE1207","Software Process & Quality Assurance")]:
            c,_=Course.objects.get_or_create(course_code=code, defaults={"course_name":name, "programme":prog})
            courses.append(c)

        lec_user=User.objects.filter(role='LECTURER').first()
        lec=Lecturer.objects.filter(user=lec_user).first() if lec_user else None

        for i in range(1,21):
            reg=f"UICT/2025/DSWE/{i:04d}"
            uname=reg
            if not User.objects.filter(username=uname).exists():
                full_name=f"Student {i} Name"
                u=User.objects.create_user(username=uname, password=full_name, role='STUDENT')
                s=Student.objects.create(user=u, registration_number=reg, first_name=f"Student{i}", last_name="Name", email=f"s{i}@uict.ac.ug", programme=prog, year_of_study=2)
                for c in courses:
                    Enrollment.objects.get_or_create(student=s, course=c)

        if lec:
            today=date.today()
            for idx,c in enumerate(courses):
                Lecture.objects.get_or_create(course=c, lecturer=lec, lecture_date=today, start_time=time(8+idx*2,0), end_time=time(10+idx*2,0), defaults={"room":f"Lab {idx+1}", "status":"SCHEDULED"})

        self.stdout.write(self.style.SUCCESS("Seed done: admin/admin123, students UICT/2026/DSWE/0001 password 'Student 1 Name', lecturers LEC001 / Lecturer123"))