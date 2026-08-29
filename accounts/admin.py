from django.contrib import admin
from .models import User, Student, Lecturer

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'is_active']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'full_name', 'email', 'programme', 'year_of_study']
    search_fields = ['registration_number', 'first_name']

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ['staff_number', 'full_name', 'email', 'department']