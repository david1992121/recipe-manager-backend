from django.test import TestCase
from basics.models import AmountUnit, Currency
from foods.models import Combination, Ingredient, Recipe
from django.urls import reverse


class RecipeAppTest(TestCase):
    """
    A parent class of all the following test classes

    It initializes some values and objects used for the tests.
    """

    def set_values(self):
        """ Set the sample values for creating mock data for testing. """
        self.currency_name = "euro"
        self.currency_code = "EUR"
        self.currency_rate = "1.0"
        self.unit_name = "grams"
        self.ingredient_name = "carrot"
        self.ingredient_article_number = "1111111111111"
        self.ingredient_cost = 1
        self.ingredient_amount = 500
        self.recipe_name = "Carrot Cake"
        self.combination_amount = 100

    def setUp(self):
        """ Create an `AmountUnit`, `Currency`, `Ingredient`, and `Recipe` object using sample values. """
        self.set_values()
        self.currency = Currency.objects.create(
            name=self.currency_name, code=self.currency_code, rate=self.currency_rate)
        self.amount_unit = AmountUnit.objects.create(name=self.unit_name)

        self.ingredient = Ingredient.objects.create(
            name=self.ingredient_name,
            article_number=self.ingredient_article_number,
            cost=self.ingredient_cost,
            currency=self.currency,
            amount=self.ingredient_amount,
            amount_unit=self.amount_unit
        )

        self.recipe = Recipe.objects.create(
            name=self.recipe_name
        )

        self.combination = Combination.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            amount=self.combination_amount
        )

    def get_combination_cost(self, cur_amount):
        ''' Calculate the cost of the combination using the initialized ingredient. '''
        per_amount = float(self.ingredient_cost / self.ingredient_amount)
        return float(self.currency_rate) * cur_amount * per_amount
