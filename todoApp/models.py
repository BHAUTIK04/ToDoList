from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import now
# Create your models here.

class tasklist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=False, null=False)
    description = models.CharField(max_length=256, blank=False, null=False)
    deadline = models.DateTimeField(blank=True, null=True)
    
    status = models.BooleanField(default=False)
    status_change_by = models.ForeignKey(User, related_name='%(class)s_status_changed', null=True)
    status_change_at = models.DateTimeField(blank=False, null=True)
    
    created_at = models.DateTimeField(default= now, blank=False)
    edited_at = models.DateTimeField(blank=True,null=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    