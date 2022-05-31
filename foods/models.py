from django.db import models
from basics.models import AmountUnit, Currency
from basics.validators import rate_validator
from .validators import article_number_validator
from django.db import transaction
from foods.utils import convert_to_str


class Ingredient(models.Model):
    """
    A model for ingredients

    Each ingredient havs its own name, article number, and cost.
    The cost is defined as the following format.

    [`cost`][`currency`] per [`amount`][`amount_unit`]

    For example, the ingredient with the name 'carrot' has a cost of 1 EUR per 500 grams.

    The model has two foreign key fields, `currency` and `amount_unit`, which are related \
        with the models in `basics` app.

    """

    def __init__(self, *args, **kwargs):
        ''' Set the initial amount and unit value. '''
        super().__init__(*args, **kwargs)
        self.initial_cost = self.get_cost()

    def __str__(self):
        return self.name

    name = models.CharField(unique=True, max_length=255)
    article_number = models.CharField(
        unique=True, max_length=20, validators=[article_number_validator])
    cost = models.DecimalField(max_digits=11, decimal_places=3)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    amount_unit = models.ForeignKey(AmountUnit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ingredient"
        verbose_name_plural = "ingredients"

    def get_cost(self):
        ''' Get the cost in EUR per amount. '''
        return float(self.cost) * float(self.currency.rate) / float(self.amount)

    def update_cost(self, cost_delta):
        ''' Update the costs of the related combinations and recipes. '''
        combinations = Combination.objects.filter(ingredient_id=self.id)

        for combination_item in combinations:
            # update the combination
            combination_item.save()

            # update the cost in recipe
            delta_cost = cost_delta * float(combination_item.amount)
            combination_item.recipe.cost = convert_to_str(
                float(combination_item.recipe.cost) + delta_cost)
            combination_item.recipe.save(update_fields=["cost"])

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

            if self.id is not None:
                self.per_cost = self.get_cost()
                cost_delta = self.per_cost - self.initial_cost
                if abs(cost_delta) > 10e-8:
                    self.update_cost(cost_delta)


class Recipe(models.Model):
    """
    A model for Recipes

    A recipe has its name and contains the list of ingredients with the amounts needed.
    The model has a many-to-many relationship with the `Ingredient` model through the `Combination` model.
    """

    def __str__(self):
        return self.name

    name = models.CharField(unique=True, max_length=255)
    cost = models.CharField(
        max_length=100, validators=[rate_validator], null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "recipe"
        verbose_name_plural = "recipes"


class Combination(models.Model):
    """
    A model for mediating the relationship between the `Recipe` and `Ingredient` model

    Each combination indicates that the recipe A has the amount B of the ingredient C.
    For example, the recipe for 'Carrot Cake' contains 100 grams of 'carrot'.
    """

    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="combinations")
    amount = models.DecimalField(max_digits=11, decimal_places=3)
    cost = models.CharField(max_length=100, validators=[rate_validator])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'], name='recipe_ingredient_combination'
            )
        ]
        verbose_name = "combination"
        verbose_name = "combinations"

    def save(self, *args, **kwargs):
        '''
        Calculate the cost of the current combination.

        The currency of the cost is EUR.
        '''

        combination_cost = self.ingredient.get_cost() * float(self.amount)
        self.cost = convert_to_str(combination_cost)
        super().save(*args, **kwargs)
