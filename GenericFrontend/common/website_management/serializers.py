from rest_framework import serializers
from . models import *


# class InvoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice.
#         fields = '__all__'


class WebsiteLaunchInfoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteLaunchInfoStatus
        fields = '__all__'


class WebsiteDowntimeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteDowntimeStatus
        fields = '__all__'
