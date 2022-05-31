import json
from django.urls import reverse

from foods.models import Combination
from .base import RecipeAppTest


class IngredientViewTest(RecipeAppTest):
    '''
    Tests for the GET, POST, RETRIEVE, PATCH, PUT, DELETE method
    '''

    def test_list(self):
        response = self.client.get(reverse('ingredient-list'))
        self.assertEqual(response.status_code, 200)
        ingredients = json.loads(response.content)
        self.assertEqual(len(ingredients), 1)
        self.assertEqual(ingredients[0]['name'], self.ingredient_name)

    def test_create(self):
        response = self.client.post(reverse('ingredient-list'), {
            "name": "new-ingredient",
            "article_number": "12345678",
            "cost": 1,
            "currency_id": self.currency.id,
            "amount": 500,
            "amount_unit_id": self.amount_unit.id
        })
        self.assertEqual(response.status_code, 201)
        created_one = json.loads(response.content)
        self.check_delete(created_one['id'])

    def test_retrieve(self):
        response = self.client.get(reverse('ingredient-detail', kwargs={
            'pk': self.ingredient.id,
        }))
        self.assertEqual(response.status_code, 200)
        ingredient = json.loads(response.content)
        self.assertEqual(ingredient['name'], self.ingredient_name)
        self.assertEqual(ingredient['article_number'],
                         self.ingredient_article_number)

    def test_partial_update(self):
        new_name = "new-ingredient"
        response = self.client.patch(reverse('ingredient-detail', kwargs={
            'pk': self.ingredient.id,
        }), {
            'name': new_name
        }, content_type='application/json')
        self.ingredient_name = new_name
        self.assertEqual(response.status_code, 200)
        self.test_retrieve()

    def test_update(self):
        new_article_number = "1234567890123"
        response = self.client.put(reverse('ingredient-detail', kwargs={
            'pk': self.ingredient.id,
        }), {
            "name": self.ingredient_name,
            "article_number": new_article_number,
            "cost": 1,
            "currency_id": self.currency.id,
            "amount": 500,
            "amount_unit_id": self.amount_unit.id
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.ingredient_article_number = new_article_number
        self.test_retrieve()

    def test_delete(self):
        self.check_delete(self.ingredient.id)

    def check_delete(self, id):
        response = self.client.delete(reverse('ingredient-detail', kwargs={
            'pk': id,
        }))
        if Combination.objects.filter(ingredient_id=id).count() > 0:
            self.assertEqual(response.status_code, 409)
        else:
            self.assertEqual(response.status_code, 204)
            response = self.client.get(reverse('ingredient-detail', kwargs={
                'pk': id,
            }))
            self.assertEqual(response.status_code, 404)


class RecipeViewTest(RecipeAppTest):
    '''
    Tests for the GET, POST, RETRIEVE, PATCH, PUT, DELETE method
    '''

    def test_list(self):
        response = self.client.get(reverse('recipe-list'))
        self.assertEqual(response.status_code, 200)
        recipes = json.loads(response.content)
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0]['name'], self.recipe_name)

    def test_create(self):
        new_amount = 600
        response = self.client.post(reverse('recipe-list'), {
            "name": "new-recipe",
            "combinations": [
                {
                    "ingredient_id": self.ingredient.id,
                    "amount": new_amount
                }
            ]
        }, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # check if the recipe total cost is calculated correctly
        created_recipe = json.loads(response.content)
        combination_cost = self.get_combination_cost(new_amount)
        self.assertEqual(float(created_recipe['cost']), combination_cost)

    def test_retrieve(self):
        response = self.client.get(reverse('recipe-detail', kwargs={
            'pk': self.recipe.id,
        }))
        self.assertEqual(response.status_code, 200)
        recipe = json.loads(response.content)
        self.assertEqual(recipe['name'], self.recipe_name)

    def test_partial_update(self):
        new_name = "new-recipe"
        response = self.client.patch(reverse('recipe-detail', kwargs={
            'pk': self.recipe.id,
        }), {
            'name': new_name
        }, content_type='application/json')
        self.recipe_name = new_name
        self.assertEqual(response.status_code, 200)
        self.test_retrieve()

    def test_update(self):

        response = self.client.put(reverse('recipe-detail', kwargs={
            'pk': self.recipe.id,
        }), {
            "name": self.recipe_name,
            "combinations": [
                {
                    "ingredient_id": self.ingredient.id,
                    "amount": 700
                }
            ]
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.delete(reverse('recipe-detail', kwargs={
            'pk': self.recipe.id,
        }))
        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse('recipe-detail', kwargs={
            'pk': self.recipe.id,
        }))
        self.assertEqual(response.status_code, 404)
