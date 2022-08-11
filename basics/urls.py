from django.urls import path

from basics.views import AmountUnitView, CurrencyView, handle_delay

urlpatterns = [
    path('amount_units', AmountUnitView.as_view(), name="amount_unit_list"),
    path('currencies', CurrencyView.as_view(), name="currency_list"),
    path('delay', handle_delay, name="delay")
]
