from basics.tests.base import ValidatorTest
from foods.validators import article_number_validator


class CurrencyCodeValidatorTest(ValidatorTest):
    def setUp(self):
        super().setUp(article_number_validator)

    def test_cases(self):
        self.check_value("1234567w", False)
        self.check_value("234223", False)
        self.check_value("5901234123457", True)
        self.check_value("65833254", True)
