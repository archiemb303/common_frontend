from django.db import models
from datetime import datetime, timedelta

'''
This File Contains Following Tables
1. WdCountries
2.WdStates
3.WdCites
'''


# Create your models here.
class Currencies(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency_name = models.CharField(max_length=100, default=None)
    value_of_one_credit_point = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.currency_id)


class Geos(models.Model):
    geo_id = models.AutoField(primary_key=True)
    geo_name = models.CharField(max_length=100, default=None)
    geo_currency = models.ForeignKey(Currencies, default=3, on_delete=models.CASCADE)
    tax_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.geo_id)

class Countries(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100)
    country_code_iso3 = models.CharField(max_length=100, default=None, blank=True, null=True)
    country_code_iso2 = models.CharField(max_length=100, default=None, blank=True, null=True)
    currency = models.CharField(max_length=100,default=None, blank=True, null=True)
    phone_code = models.CharField(max_length=100,default=None, blank=True, null=True)
    added_by = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)
    geo_id = models.ForeignKey(Geos,default=2,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.country_id)


class States(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=100)
    country_id = models.ForeignKey(Countries, on_delete=models.CASCADE)
    added_by = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.state_id)


class Cities(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    state_id = models.ForeignKey(States, on_delete=models.CASCADE)
    added_by = models.CharField(max_length=100, default=None)
    added_date = models.DateTimeField(default=datetime.now)
    last_modified_by = models.CharField(max_length=100, default=None)
    last_modified_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.city_id)
