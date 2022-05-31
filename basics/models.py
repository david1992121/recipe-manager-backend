from django.db import models

from basics.validators import currency_code_validator, rate_validator


class AmountUnit(models.Model):
    """
    A model representing the units of amount

    It contains the `name` field that indicates the unit name.
    For example, it can be 'grams', 'kilograms', 'liter', etc.
    """

    def __str__(self):
        return self.name

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "unit of amount"
        verbose_name_plural = "units of amount"


class Currency(models.Model):
    """
    A model containing the list of currency codes

    The each currency has its name, code, and the exchange rate to EUR.
    """

    def __str__(self):
        return self.name

    name = models.CharField(max_length=10, unique=True)
    code = models.CharField(max_length=10, unique=True,
                            validators=[currency_code_validator])
    rate = models.CharField(max_length=50, validators=[rate_validator])

    class Meta:
        verbose_name = "currency"
        verbose_name_plural = "currencies"
