from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from .filters import IngredientFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ingredient, Recipe, Combination
from .serializers import IngredientSerializer, RecipeSerializer, FoodPagination


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    pagination_class = FoodPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ('-updated_at')

    def destroy(self, request, pk):
        # check if any combination has the ingredient to be removed
        if Combination.objects.filter(ingredient_id=pk).count() > 0:
            return Response(status=status.HTTP_409_CONFLICT)
        else:
            return super().destroy(request, pk)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = FoodPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ('-updated_at')
