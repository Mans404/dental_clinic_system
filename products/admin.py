from django.contrib import admin
from .models import Product, ProductPriceTier


class ProductPriceTierInline(admin.TabularInline):
	model = ProductPriceTier
	extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'quantity', 'price')
	inlines = [ProductPriceTierInline]
