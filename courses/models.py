from django.db import models
class Course(models.Model):
    course_code=models.CharField(max_length=20, unique=True)
    course_name=models.CharField(max_length=200)
    programme=models.ForeignKey('programmes.Programme', on_delete=models.CASCADE, null=True)
    year_of_study=models.IntegerField(default=1)
    semester=models.IntegerField(default=1)
    status=models.CharField(max_length=10, default='ACTIVE')
    def __str__(self): return f"{self.course_code} {self.course_name}"

class Enrollment(models.Model):
    student=models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=('student','course')