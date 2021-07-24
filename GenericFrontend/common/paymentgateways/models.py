from django.db import models
from datetime import datetime
import uuid
from django.contrib.postgres.fields import JSONField
from common.finance.ownaccountsandledger.models import SelfAccounts
from common.location.models import Currencies, Countries
from common.sessionmanagement.models import UserSessions

# Create your models here.


# PaymentGatewayStatus
class PaymentGatewayStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(max_length=100, default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.status_id)


# PaymentGatewayProviders
class PaymentGatewayProviders(models.Model):
    provider_id = models.AutoField(primary_key=True)
    provider_name = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(max_length=100, default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.provider_id)


# PaymentGateways
class PaymentGateways(models.Model):
    pg_id = models.AutoField(primary_key=True)
    pg_name = models.CharField(max_length=100, default=None)
    pg_cred = JSONField(max_length=1000, default=None)
    associated_self_financial_accounts = models.ForeignKey(SelfAccounts, on_delete=models.CASCADE)
    pg_status = models.ForeignKey(PaymentGatewayStatus, on_delete=models.CASCADE)
    pg_provider = models.ForeignKey(PaymentGatewayProviders, on_delete=models.CASCADE)
    added_date = models.DateTimeField(max_length=100, default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.pg_id)


# PaymentGatewayTransactionStatus
class PaymentGatewayTransactionStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(max_length=100, default=datetime.now)
    added_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.status_id)


# PaymentGatewayTransactions
class PaymentGatewayTransactions(models.Model):
    pg_transaction_id = models.CharField(primary_key=True, blank=True, max_length=100, unique=True, default=uuid.uuid4, editable=False)
    pg_id = models.ForeignKey(PaymentGateways, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(max_length=100, default=datetime.now)
    amount = models.FloatField(default=0.0)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    customer_country_id = models.ForeignKey(Countries, on_delete=models.CASCADE)
    transaction_status = models.ForeignKey(PaymentGatewayTransactionStatus, on_delete=models.CASCADE)
    request_object = models.CharField(max_length=10000, default=None, null=True)
    response_object = models.CharField(max_length=10000, default=None, null=True)
    actual_transaction_amount = models.FloatField(default=0.0)
    actual_transaction_currency = models.ForeignKey(Currencies, on_delete=models.CASCADE, related_name='actual_transaction_currency', null=True, default= None)

    def __str__(self):
        return str(self.pg_transaction_id)

