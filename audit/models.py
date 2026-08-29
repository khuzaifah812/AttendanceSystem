from django.db import models
from django.conf import settings
class AuditLog(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action=models.CharField(max_length=50)
    timestamp=models.DateTimeField(auto_now_add=True)
    ip_address=models.GenericIPAddressField(null=True, blank=True)
    description=models.TextField(blank=True)