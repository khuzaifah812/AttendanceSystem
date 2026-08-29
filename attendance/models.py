from django.db import models
class Attendance(models.Model):
    student=models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    lecture=models.ForeignKey('lectures.Lecture', on_delete=models.CASCADE)
    check_in_time=models.DateTimeField(auto_now_add=True)
    attendance_date=models.DateField(auto_now_add=True)
    latitude=models.DecimalField(max_digits=10, decimal_places=8)
    longitude=models.DecimalField(max_digits=11, decimal_places=8)
    gps_accuracy=models.FloatField(default=0)
    distance_from_campus=models.FloatField(default=0)
    location_verified=models.BooleanField(default=False)
    ip_address=models.GenericIPAddressField(null=True)
    user_agent=models.TextField(blank=True)
    status=models.CharField(max_length=10, default='PRESENT')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=('student','lecture')