from rest_framework import serializers
from . models import *

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'
        # fields = ('country_id','country_name')


class StatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = '__all__'
        # fields = ('state_id','state_name','country_id')


class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        # fields = ('city_id','city_name', 'state_id')
        fields = '__all__'


class StatesAndCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = '__all__'
        depth = 1


class CitiesAndStatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = '__all__'
        depth = 2


class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = '__all__'


class GeosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geos
        fields = '__all__'
