from django.db import models
from datetime import datetime
from common.registration.models import UserProfile
from common.apiauthentication.models import Vendor
#Create your models here.

class UserSessionsStatus(models.Model):
    status_id = models.AutoField(primary_key = True)
    status_name = models.CharField(max_length=100, default =  None)
    added_by = models.CharField(max_length=100, default = 's')
    added_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default = 's')
    last_modified_date = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return str(self.status_id)

class UserSessions(models.Model):
    session_id = models.AutoField(primary_key=True)
    # profile_id = models.IntegerField(default =  None)
    profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=datetime.now)
    logout_time = models.DateTimeField(default=datetime.now)
    session_key = models.CharField(max_length = 100, default = None)
    vendor = models.ForeignKey(Vendor, default=1, on_delete=models.CASCADE)
    login_source = models.CharField(max_length=100, default='mobile') #website/iOSaoo/Android App
    login_type = models.CharField(max_length = 100, default='native')  #natice/google/facebook/linkedIn
    logout_type = models.CharField(max_length=100, default='current_session') #logout from all devices/logout from this device
    last_activity_time = models.DateTimeField(default=datetime.now)
    status_id = models.ForeignKey(UserSessionsStatus,on_delete=models.CASCADE) #active/inactive/expired
    added_by = models.CharField(max_length=100, default='s')
    added_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default='s')
    last_modified_date = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return str(self.session_id)
