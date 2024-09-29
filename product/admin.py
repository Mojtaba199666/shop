from django.contrib import admin
from .models import Brand, Product, Category, ProductLine


class ProductLineInline(admin.TabularInline):
    model = ProductLine


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ProductLine)
