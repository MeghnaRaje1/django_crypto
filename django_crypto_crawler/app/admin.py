
from django.contrib import admin
from .models import Product, HistoricalData

admin.site.register(Product)
admin.site.register(HistoricalData)
