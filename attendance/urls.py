from django.urls import path
from .views import ActiveAttendanceAPI, CheckInAPI, StudentHistoryAPI
urlpatterns=[
    path('attendance/active/', ActiveAttendanceAPI.as_view()),
    path('attendance/check-in/', CheckInAPI.as_view()),
    path('student/attendance-history/', StudentHistoryAPI.as_view()),
]