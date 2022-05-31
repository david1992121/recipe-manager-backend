from django_filters import FilterSet, CharFilter
from .models import Ingredient


class IngredientFilter(FilterSet):
    class Meta:
        model = Ingredient
        fields = {
            'name': ['contains'],
            'article_number': ['contains']
        }
