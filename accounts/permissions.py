from rest_framework.permissions import BasePermission
class IsAdmin(BasePermission):
    def has_permission(self, r, v): return r.user.is_authenticated and r.user.role=='ADMIN'
class IsLecturer(BasePermission):
    def has_permission(self, r, v): return r.user.is_authenticated and r.user.role=='LECTURER'
class IsStudent(BasePermission):
    def has_permission(self, r, v): return r.user.is_authenticated and r.user.role=='STUDENT'