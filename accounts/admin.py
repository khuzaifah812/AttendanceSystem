from django.contrib import admin
from .models import User, Student, Lecturer

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'is_active']
    list_filter = ['role']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'full_name', 'email', 'program']
    search_fields = ['registration_number', 'first_name']
    exclude = ['user']  # Hides the confusing User dropdown

    def save_model(self, request, obj, form, change):
        if not obj.user_id:  # Only on create
            username = obj.registration_number.replace('/', '_').lower()
            # Ensure unique
            if User.objects.filter(username=username).exists():
                username = f"{username}_{obj.registration_number[-4:]}"
            
            user = User.objects.create_user(
                username=username,
                email=obj.email,
                password="student123",
                role="STUDENT"
            )
            obj.user = user
        super().save_model(request, obj, form, change)

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ['staff_number', 'full_name', 'email', 'department']
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            user = User.objects.create_user(
                username=obj.staff_number.lower(),
                email=obj.email,
                password="lecturer123",
                role="LECTURER"
            )
            obj.user = user
        super().save_model(request, obj, form, change)