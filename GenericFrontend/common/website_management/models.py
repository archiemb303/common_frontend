from django.db import models
# Create your models here.


# WebsiteLaunchInfoStatus
class WebsiteLaunchInfoStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.status_id)


# WebsiteLaunchInfo
class WebsiteLaunchInfo(models.Model):
    launch_info_id = models.AutoField(primary_key=True)
    launch_date = models.DateTimeField(max_length=100, default=None, null=True)
    launch_info_status = models.ForeignKey(WebsiteLaunchInfoStatus, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.launch_info_id)


# WebsiteDowntimeStatus
class WebsiteDowntimeStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.status_id)


# WebsiteDowntime
class WebsiteDowntime(models.Model):
    downtime_info_id = models.AutoField(primary_key=True)
    downtime_start_datetime = models.DateTimeField(max_length=100, default=None, null=True)
    downtime_end_datetime = models.DateTimeField(max_length=100, default=None, null=True)
    downtime_info_status = models.ForeignKey(WebsiteDowntimeStatus, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.downtime_info_id)
