from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Lecturer

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (('Role', {'fields': ('role','full_name')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Role', {'fields': ('role','full_name')}),)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'reg_number']
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ['get_username']
    def get_username(self, obj):
        return obj.user.username