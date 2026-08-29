from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.student_list, name='manage_students'),
    path('students/add/', views.student_add, name='manage_student_add'),
    path('lecturers/', views.lecturer_list, name='manage_lecturers'),
    path('lecturers/add/', views.lecturer_add, name='manage_lecturer_add'),
    path('courses/', views.course_list, name='manage_courses'),
    path('courses/add/', views.course_add, name='manage_course_add'),
    path('lectures/', views.lecture_list, name='manage_lectures'),
    path('lectures/add/', views.lecture_add, name='manage_lecture_add'),
]