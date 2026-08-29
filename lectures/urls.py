from django.urls import path
from .views import LecturerLecturesAPI, StartAttendanceAPI, EndAttendanceAPI, LectureAttendanceListAPI
urlpatterns=[
    path('lecturer/lectures/', LecturerLecturesAPI.as_view()),
    path('lecturer/lectures/<int:id>/start-attendance/', StartAttendanceAPI.as_view()),
    path('lecturer/lectures/<int:id>/end-attendance/', EndAttendanceAPI.as_view()),
    path('lecturer/lectures/<int:id>/attendance/', LectureAttendanceListAPI.as_view()),
]