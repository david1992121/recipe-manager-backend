from django.contrib import admin

from .models import Ingredient, Recipe

admin.site.register(Ingredient, admin.ModelAdmin)
admin.site.register(Recipe, admin.ModelAdmin)
