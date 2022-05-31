import random
from django.conf import settings
from django.core.management.base import CommandError
from foods.models import Recipe, Ingredient, Combination
from foods.utils import convert_to_str
from .seed_ingredient import SeedCommand


class Command(SeedCommand):
    help = "Seed the recipe data"

    def handle(self, *args, **options):
        ingredient_len = Ingredient.objects.count()
        max_combination_num = min(10, ingredient_len)

        if ingredient_len == 0:
            raise CommandError(
                "Please seed the ingredient data first")

        for _ in range(options['number']):
            # create a recipe first
            recipe = Recipe.objects.create(
                name=self.get_name()
            )

            # get random number of ingredients to be combined
            combination_num = random.randint(1, max_combination_num)

            # get random ids of the ingredients
            ingredient_ids = random.sample(
                range(1, ingredient_len + 1), combination_num)

            # create combinations
            recipe_total = 0
            for ingredient_id in ingredient_ids:
                new_combination = Combination.objects.create(
                    ingredient_id=ingredient_id,
                    recipe_id=recipe.id,
                    amount=random.randrange(10, 100, 10)
                )
                recipe_total += float(new_combination.cost)
            recipe.cost = convert_to_str(recipe_total)
            recipe.save()
