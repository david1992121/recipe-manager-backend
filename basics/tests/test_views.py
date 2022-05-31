import json
from django.urls import reverse
from .base import BasicAppTest


class AmountUnitViewTest(BasicAppTest):
    def test_list(self):
        response = self.client.get(reverse('amount_unit_list'))
        self.assertEqual(response.status_code, 200)
        amount_units = json.loads(response.content)
        self.assertEqual(len(amount_units), 1)
        self.assertEqual(amount_units[0]['name'], self.unit_name)


class CurrenyViewTest(BasicAppTest):
    def test_list(self):
        response = self.client.get(reverse('currency_list'))
        self.assertEqual(response.status_code, 200)
        currencies = json.loads(response.content)
        self.assertEqual(len(currencies), 1)
        self.assertEqual(currencies[0]['name'], self.currency_name)
        self.assertEqual(currencies[0]['code'], self.currency_code)
        self.assertEqual(currencies[0]['rate'], self.currency_rate)
