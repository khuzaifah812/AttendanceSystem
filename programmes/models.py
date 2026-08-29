from django.db import models
class Programme(models.Model):
    name=models.CharField(max_length=200, unique=True)
    code=models.CharField(max_length=20, unique=True)
    def __str__(self): return self.name