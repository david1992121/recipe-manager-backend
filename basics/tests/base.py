from django.test import TestCase

from basics.models import AmountUnit, Currency
from django.core.exceptions import ValidationError


class BasicAppTest(TestCase):
    """
    A parent class of the test classes for models and views

    It initializes some values and objects used for the tests.
    """

    def set_values(self):
        """ Set the sample values for creating mock data for testing. """
        self.unit_name = "grams"
        self.currency_name = "euro"
        self.currency_code = "EUR"
        self.currency_rate = "1.0"

    def setUp(self):
        """ Create an `AmountUnit` and `Currency` object using sample values. """
        self.set_values()
        self.amount_unit = AmountUnit.objects.create(name=self.unit_name)
        self.currency = Currency.objects.create(
            name=self.currency_name, code=self.currency_code, rate="1.0")


class ValidatorTest(TestCase):
    """
    A parent class of all the test classes for validators
    """

    def setUp(self, validator_func):
        self.validator = validator_func

    def check_value(self, value, expected_result):
        no_error = True
        try:
            self.validator(value)
        except ValidationError:
            no_error = False
        self.assertEqual(no_error, expected_result)
