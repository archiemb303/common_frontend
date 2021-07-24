from django.db import models
from datetime import datetime
from common.registration.models import UserProfile

# Create your models here.


# StaffStatus
class StaffStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(max_length=100, default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.status_id)


# Staffs
class Staffs(models.Model):
    staff_id = models.AutoField(primary_key=True)
    staff_profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    staff_registration_date = models.DateTimeField(max_length=100, default=datetime.now)
    staff_removal_date = models.DateTimeField(max_length=100, default=datetime.now)
    staff_status = models.ForeignKey(StaffStatus, on_delete=models.CASCADE)
    added_date = models.DateTimeField(max_length=100, default=datetime.now)
    added_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='staff_added_by')
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='staff_last_modified_by')

    def __str__(self):
        return str(self.staff_id)
