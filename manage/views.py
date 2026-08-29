from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User, Student, Lecturer
from programmes.models import Programme
from lectures.models import Lecture
# If your model names are different, tell me!

@login_required
def student_list(request):
    students = Student.objects.all().select_related('user', 'programme')
    return render(request, 'manage/student_list.html', {'students': students})

@login_required
def student_add(request):
    programmes = Programme.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        reg_no = request.POST['reg_number']
        prog_id = request.POST['programme']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password, role='STUDENT')
        Student.objects.create(user=user, reg_number=reg_no, programme_id=prog_id)
        messages.success(request, 'Student added!')
        return redirect('/manage/students/')
    return render(request, 'manage/student_form.html', {'programmes': programmes})

@login_required
def lecturer_list(request):
    lecturers = Lecturer.objects.all().select_related('user')
    return render(request, 'manage/lecturer_list.html', {'lecturers': lecturers})

@login_required
def lecturer_add(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password, role='LECTURER')
        Lecturer.objects.create(user=user)
        messages.success(request, 'Lecturer added!')
        return redirect('/manage/lecturers/')
    return render(request, 'manage/lecturer_form.html')

@login_required
def course_list(request):
    courses = Programme.objects.all()
    return render(request, 'manage/course_list.html', {'courses': courses})

@login_required
def course_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']
        Programme.objects.create(name=name, code=code)
        return redirect('/manage/courses/')
    return render(request, 'manage/course_form.html')

@login_required
def lecture_list(request):
    lectures = Lecture.objects.all().order_by('-id')[:50]
    return render(request, 'manage/lecture_list.html', {'lectures': lectures})

@login_required
def lecture_add(request):
    programmes = Programme.objects.all()
    lecturers = Lecturer.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        prog_id = request.POST['programme']
        lect_id = request.POST['lecturer']
        Lecture.objects.create(title=title, programme_id=prog_id, lecturer_id=lect_id)
        return redirect('/manage/lectures/')
    return render(request, 'manage/lecture_form.html', {'programmes': programmes, 'lecturers': lecturers})