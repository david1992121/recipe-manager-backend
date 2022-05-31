from rest_framework.generics import ListAPIView
from rest_framework import filters
from basics.serializers import AmountUnitSerializer, CurrencySerializer
from .models import AmountUnit, Currency


class AmountUnitView(ListAPIView):
    queryset = AmountUnit.objects.all()
    serializer_class = AmountUnitSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ('id', )


class CurrencyView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ('id', )
