from django.contrib import admin

from basics.models import AmountUnit, Currency

admin.site.register(AmountUnit, admin.ModelAdmin)
admin.site.register(Currency, admin.ModelAdmin)
