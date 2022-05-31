from rest_framework import serializers
from .models import AmountUnit, Currency


class AmountUnitSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AmountUnit


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Currency
