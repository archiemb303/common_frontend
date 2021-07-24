from rest_framework import serializers
from .models import *


class SuperNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperNotifications
        fields = '__all__'


class IndividualNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualNotifications
        fields = '__all__'


class IndividualNotificationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualNotificationStatus
        fields = '__all__'


class SuperNotificationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperNotificationStatus
        fields = '__all__'


class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = '__all__'


class NotificationDistributionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationDistributionType
        fields = '__all__'
