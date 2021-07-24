from rest_framework import serializers
from . models import *


class PaymentGatewaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateways
        fields = '__all__'


class PaymentGatewayTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayTransactions
        fields = '__all__'


class PaymentGatewayTransactionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayTransactionStatus
        fields = '__all__'


class PaymentGatewayStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayStatus
        fields = '__all__'


class PaymentGatewayProvidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayProviders
        fields = '__all__'
