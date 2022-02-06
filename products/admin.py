from django.contrib import admin
from .models import Product, Category, Manufacturer, TyreSize

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'ean',
        'manufacturer',
        'size',
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

class TyreSizeAdmin(admin.ModelAdmin):
    list_display = (
        'full_size_code',
        'full_size_display',
    )

    ordering = ('rim_size', 'width', 'heigth')

admin.site.register(TyreSize, TyreSizeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
