from django.db import models

# Create your models here.
'''
This File Contains Following Tables
1.VendorStatus
2.Vendor
3.TokenStatus
4.TokenType
5.ApiTokens
'''


class VendorStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.status_id)


class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    vendor_name = models.CharField(max_length=100, blank=True)
    vendor_status = models.ForeignKey(VendorStatus,
                                      on_delete=models.CASCADE)  # Active, Inactive, PendingActivation, Suspended
    def __str__(self):
        return str(self.vendor_id)


class TokenStatus(models.Model):
    # Active, Inactive, PendingActivation, Suspended
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.status_id)


class TokenType(models.Model):
    # webapp, mobileapp, restAPIclient
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.type_id)


class ApiTokens(models.Model):
    token_id = models.AutoField(primary_key=True)
    token_string = models.CharField(max_length=100, default="")
    token_type = models.ForeignKey(TokenType, on_delete=models.CASCADE)
    token_vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    token_status_id = models.ForeignKey(TokenStatus, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.token_id)
