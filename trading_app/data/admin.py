from django.contrib import admin

from .models import Sector, Investement_Types, Stocks, Stock_Price
# Register your models here.

admin.site.register(Stock_Price)
admin.site.register(Sector)
admin.site.register(Investement_Types)
admin.site.register(Stocks)

