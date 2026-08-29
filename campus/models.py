from django.db import models
class CampusConfiguration(models.Model):
    school_name=models.CharField(max_length=200, default="UICT")
    latitude=models.DecimalField(max_digits=10, decimal_places=8)
    longitude=models.DecimalField(max_digits=11, decimal_places=8)
    allowed_radius_meters=models.IntegerField(default=200)
    status=models.CharField(max_length=10, default='ACTIVE')
    created_at=models.DateTimeField(auto_now_add=True)