from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from common.registration.models import UserProfile
# Create your models here.


class IndividualNotificationStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.status_id)


class SuperNotificationStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.status_id)


class NotificationType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.type_id)


class NotificationDistributionType(models.Model):
    distribution_type_id = models.AutoField(primary_key=True)
    distribution_type_name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.distribution_type_id)


class Algorithm(models.Model):
    algorithm_id = models.AutoField(primary_key=True)
    algorithm_name = models.CharField(max_length=100, default=None)
    type_id = models.ForeignKey(
        NotificationType, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.algorithm_id)


class SuperNotifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    type_id = models.ForeignKey(
        NotificationType, on_delete=models.CASCADE, default=None)
    distribution_type_id = models.ForeignKey(
        NotificationDistributionType, on_delete=models.CASCADE, default=None)
    notification_text = ArrayField(models.CharField(max_length=200, default=None, null=True),default=None,null=True)
    redirection_url = models.CharField(max_length=200, default=None)
    notification_status = models.ForeignKey(
        SuperNotificationStatus, on_delete=models.CASCADE, default=None)
    notifier_profile_id = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, default=None, null=True, related_name='notifier_id')  # sender-should not be null for user-generated notifications
    notified_profile_id = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, default=None, null=True, related_name='notified_id')  # receiver-should not be null for individually targeted
    algorithm_id = models.ForeignKey(Algorithm, on_delete=models.CASCADE, default=None, null=True)
    comments = models.CharField(max_length=200, default=None, null=True)
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.ForeignKey(UserProfile, default=None, null=True, on_delete=models.CASCADE,
                                 related_name='notification_creator')
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.ForeignKey(UserProfile, default=None, null=True, on_delete=models.CASCADE,
                                         related_name='notification_modifier')

    def __str__(self):
        return str(self.notification_id)


class IndividualNotifications(models.Model):
    individual_notification_id = models.AutoField(primary_key=True)
    super_notification_id = models.ForeignKey(
        SuperNotifications, on_delete=models.CASCADE, default=None)
    notification_status = models.ForeignKey(
        IndividualNotificationStatus, on_delete=models.CASCADE, default=None)
    profile_id = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, default=None, related_name='individual_profile_id')  # send
    added_date = models.DateTimeField(default=datetime.now)
    added_by = models.ForeignKey(UserProfile, default=None, null=True, on_delete=models.CASCADE,
                                 related_name='notification_creator_user')
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.ForeignKey(UserProfile, default=None, null=True, on_delete=models.CASCADE,
                                         related_name='notification_modifier_user')

    def __str__(self):
        return str(self.individual_notification_id)
