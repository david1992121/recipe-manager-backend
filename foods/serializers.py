from rest_framework import serializers
from rest_framework import pagination
from rest_framework.response import Response

from foods.utils import convert_to_str

from .models import Combination, Ingredient, Recipe
from basics.serializers import CurrencySerializer, AmountUnitSerializer
from django.db import transaction


class FoodPagination(pagination.PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'result': data
        })


class IngredientSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)
    amount_unit = AmountUnitSerializer(read_only=True)
    currency_id = serializers.IntegerField(write_only=True)
    amount_unit_id = serializers.IntegerField(write_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'article_number',
            'cost',
            'currency',
            'amount',
            'amount_unit',
            'created_at',
            'updated_at',
            'amount_unit_id',
            'currency_id'
        )
        model = Ingredient


class CombinationSerializer(serializers.ModelSerializer):
    ingredient_id = serializers.IntegerField(write_only=True)
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'ingredient_id',
            'ingredient',
            'amount',
            'cost'
        )
        model = Combination
        extra_kwargs = {
            'cost': {'read_only': True}
        }


class RecipeSerializer(serializers.ModelSerializer):
    combinations = CombinationSerializer(many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'combinations',
            'cost',
            'created_at',
            'updated_at'
        )
        model = Recipe
        extra_kwargs = {
            'cost': {'read_only': True}
        }

    def create(self, validated_data):
        combination_data = validated_data.pop('combinations')
        recipe = Recipe()
        with transaction.atomic():
            recipe = Recipe.objects.create(**validated_data)
            self.save_combinations(recipe, combination_data)
        recipe = Recipe.objects.get(pk=recipe.id)
        return recipe

    def update(self, instance, validated_data):
        if "combinations" not in validated_data.keys():
            return super().update(instance, validated_data)

        combination_data = validated_data.pop('combinations')
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            Combination.objects.filter(recipe_id=instance.id).delete()
            self.save_combinations(instance, combination_data)

        instance = Recipe.objects.get(pk=instance.id)
        return instance

    def save_combinations(self, recipe, combination_data):
        ''' Create combination objects, calculate a total cost of the recipe. '''
        recipe_total = 0
        for combination_item in combination_data:
            new_combination = Combination.objects.create(
                ingredient_id=combination_item['ingredient_id'],
                recipe_id=recipe.id,
                amount=combination_item['amount']
            )
            recipe_total += float(new_combination.cost)
        recipe.cost = convert_to_str(recipe_total)
        recipe.save()
