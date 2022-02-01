from django.contrib import admin
from .models import Product, Category, Manufacturer

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'ean',
        'size_code',
        'manufacturer',
        'name',
        'price',
        'image',
    )

    ordering = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'name',
    )

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'name',
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
