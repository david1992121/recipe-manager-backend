from django.core.management.base import BaseCommand, CommandError
from foods.models import Ingredient
from basics.models import AmountUnit, Currency
import string
import random


class SeedCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

    def get_name(self):
        length = random.randint(10, 20)
        return ''.join(random.choices(string.ascii_lowercase, k=length))


class Command(SeedCommand):
    help = "Seed the ingredient data"

    def handle(self, *args, **options):
        currency_len = Currency.objects.count()
        amount_unit_len = AmountUnit.objects.count()

        if amount_unit_len == 0 or currency_len == 0:
            raise CommandError(
                "Please seed the initial data of the amount units and currencies")

        for _ in range(options['number']):
            Ingredient.objects.create(
                name=self.get_name(),
                article_number=self.get_article_number(),
                cost=random.randint(1, 10),
                currency_id=random.randint(1, currency_len),
                amount=500,
                amount_unit_id=random.randint(1, amount_unit_len)
            )

    def get_article_number(self):
        return ''.join(random.choices(string.digits, k=13))
