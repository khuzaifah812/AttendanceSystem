from django.db import models
class Lecture(models.Model):
    STATUS=[('SCHEDULED','Scheduled'),('ATTENDANCE_NOT_STARTED','Not Started'),('ATTENDANCE_ACTIVE','Active'),('ATTENDANCE_CLOSED','Closed'),('COMPLETED','Completed'),('CANCELLED','Cancelled')]
    course=models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    lecturer=models.ForeignKey('accounts.Lecturer', on_delete=models.CASCADE)
    lecture_date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    room=models.CharField(max_length=100)
    attendance_start_time=models.DateTimeField(null=True, blank=True)
    attendance_end_time=models.DateTimeField(null=True, blank=True)
    status=models.CharField(max_length=25, choices=STATUS, default='SCHEDULED')
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.course.course_name} {self.lecture_date} {self.start_time}-{self.end_time}"