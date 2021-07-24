from rest_framework import serializers
from . models import *


class StaffsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staffs
        fields = '__all__'


class StaffStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffStatus
        fields = '__all__'
