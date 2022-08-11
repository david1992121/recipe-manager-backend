from time import sleep
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
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

@api_view(['GET'])
def handle_delay(request):
    sleep(5)
    return Response({"result": "ok"}, status=200)