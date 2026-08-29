from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    ROLE_CHOICES=[('ADMIN','Admin'),('LECTURER','Lecturer'),('STUDENT','Student')]
    role=models.CharField(max_length=10, choices=ROLE_CHOICES)
    def is_admin(self): return self.role=='ADMIN'
    def is_lecturer(self): return self.role=='LECTURER'
    def is_student(self): return self.role=='STUDENT'

class Student(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    registration_number=models.CharField(max_length=50, unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=20, blank=True)
    programme=models.ForeignKey('programmes.Programme', on_delete=models.PROTECT, null=True)
    class_name=models.CharField(max_length=100, blank=True)
    year_of_study=models.IntegerField(default=1)
    status=models.CharField(max_length=10, default='ACTIVE')
    created_at=models.DateTimeField(auto_now_add=True)
    @property
    def full_name(self): return f"{self.first_name} {self.last_name}"
    def __str__(self): return self.registration_number

class Lecturer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer_profile')
    staff_number=models.CharField(max_length=50, unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=20, blank=True)
    department=models.CharField(max_length=100)
    status=models.CharField(max_length=10, default='ACTIVE')
    created_at=models.DateTimeField(auto_now_add=True)
    @property
    def full_name(self): return f"{self.first_name} {self.last_name}"