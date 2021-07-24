from .models import *
from rest_framework import serializers

class UserSessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSessions
        # fields = ['session_key','profile_id']
        fields = '__all__'


class UserSessionsStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSessionsStatus
        fields = '__all__'