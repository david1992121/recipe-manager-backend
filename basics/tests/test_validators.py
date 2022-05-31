from .base import ValidatorTest
from basics.validators import currency_code_validator, rate_validator


class CurrencyCodeValidatorTest(ValidatorTest):
    def setUp(self):
        super().setUp(currency_code_validator)

    def test_cases(self):
        self.check_value("ETC", False)
        self.check_value("EUR", True)
        self.check_value("USD", True)


class RateValidatorTest(ValidatorTest):
    def setUp(self):
        super().setUp(rate_validator)

    def test_cases(self):
        self.check_value("test", False)
        self.check_value("-4.6", False)
        self.check_value("5.22", True)
