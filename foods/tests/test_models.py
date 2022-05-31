from .base import RecipeAppTest
from foods.models import Recipe


class IngredientModelTest(RecipeAppTest):
    def test_name(self):
        self.assertEqual(self.ingredient.name, self.ingredient_name)
        meta_data = self.ingredient._meta.get_field('name')
        self.assertEqual(meta_data.max_length, 255)
        self.assertTrue(meta_data.unique)

    def test_article(self):
        self.assertEqual(self.ingredient.article_number,
                         self.ingredient_article_number)
        meta_data = self.ingredient._meta.get_field('article_number')
        self.assertEqual(meta_data.max_length, 20)
        self.assertTrue(meta_data.unique)

    def test_cost(self):
        self.assertEqual(self.ingredient.cost, self.ingredient_cost)
        meta_data = self.ingredient._meta.get_field('cost')
        self.assertEqual(meta_data.max_digits, 11)
        self.assertTrue(meta_data.decimal_places, 3)

    def test_currency(self):
        self.assertEqual(self.ingredient.currency, self.currency)

    def test_amount(self):
        self.assertEqual(self.ingredient.amount, self.ingredient_amount)
        meta_data = self.ingredient._meta.get_field('amount')
        self.assertEqual(meta_data.default, 1)

    def test_amount_unit(self):
        self.assertEqual(self.ingredient.amount_unit, self.amount_unit)

    def test_created_at(self):
        meta_data = self.ingredient._meta.get_field('created_at')
        self.assertTrue(meta_data.auto_now_add)

    def test_updated_at(self):
        meta_data = self.ingredient._meta.get_field('updated_at')
        self.assertTrue(meta_data.auto_now)


class RecipeModelTest(RecipeAppTest):
    def test_name(self):
        self.assertEqual(self.recipe.name, self.recipe_name)
        meta_data = self.recipe._meta.get_field('name')
        self.assertEqual(meta_data.max_length, 255)
        self.assertTrue(meta_data.unique)

    def test_cost(self):
        self.assertEqual(self.recipe.cost, None)
        meta_data = self.recipe._meta.get_field('cost')
        self.assertEqual(meta_data.max_length, 100)

    def test_ingredients(self):
        recipe = Recipe.objects.get(pk=self.recipe.id)
        self.assertEqual(recipe.combinations.count(), 1)
        element = recipe.combinations.first()
        self.assertEqual(element.ingredient.id, self.ingredient.id)
        self.assertEqual(element.amount, self.combination_amount)

    def test_created_at(self):
        meta_data = self.recipe._meta.get_field('created_at')
        self.assertTrue(meta_data.auto_now_add)

    def test_updated_at(self):
        meta_data = self.recipe._meta.get_field('updated_at')
        self.assertTrue(meta_data.auto_now)


class CombinationModelTest(RecipeAppTest):
    def setUp(self):
        super().setUp()

    def test_amount(self):
        self.assertEqual(self.combination.amount, self.combination_amount)
        meta_data = self.combination._meta.get_field('amount')
        self.assertEqual(meta_data.max_digits, 11)
        self.assertTrue(meta_data.decimal_places, 3)

    def test_ingredient(self):
        self.assertEqual(self.combination.ingredient, self.ingredient)

    def test_recipe(self):
        self.assertEqual(self.combination.recipe, self.recipe)

    def test_cost(self):
        meta_data = self.combination._meta.get_field('cost')
        self.assertEqual(meta_data.max_length, 100)
        self.assertEqual(
            self.combination.cost,
            str(self.get_combination_cost(self.combination_amount))
        )
