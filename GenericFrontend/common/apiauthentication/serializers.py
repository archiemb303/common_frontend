from rest_framework import serializers
from . models import *


class VendorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorStatus
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class TokenStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenStatus
        fields = '__all__'


class TokenTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenType
        fields = '__all__'


class ApiTokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiTokens
        fields = '__all__'
