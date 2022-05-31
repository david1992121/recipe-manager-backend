from .base import BasicAppTest


class AmountUnitModelTest(BasicAppTest):
    def test_name(self):
        self.assertEqual(str(self.amount_unit), self.unit_name)
        self.assertEqual(self.amount_unit.name, self.unit_name)
        meta_data = self.amount_unit._meta.get_field('name')
        self.assertEqual(meta_data.max_length, 255)
        self.assertTrue(meta_data.unique)


class CurrencyModelTest(BasicAppTest):
    def test_name(self):
        self.assertEqual(str(self.currency), self.currency_name)
        self.assertEqual(self.currency.name, self.currency_name)
        meta_data = self.currency._meta.get_field('name')
        self.assertEqual(meta_data.max_length, 10)
        self.assertTrue(meta_data.unique)

    def test_code(self):
        self.assertEqual(self.currency.code, self.currency_code)
        meta_data = self.currency._meta.get_field('code')
        self.assertEqual(meta_data.max_length, 10)
        self.assertTrue(meta_data.unique)

    def test_rate(self):
        self.assertEqual(self.currency.rate, self.currency_rate)
        meta_data = self.currency._meta.get_field('rate')
        self.assertEqual(meta_data.max_length, 50)
