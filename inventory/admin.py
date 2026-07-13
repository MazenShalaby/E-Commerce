from django.contrib import admin

from .models import Category, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'slug']
    list_filter = ['name', 'slug']
    readonly_fields = ['slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'quantity', 'created_at', 'updated_at']
    search_fields = ['name', 'price', 'category', 'slug']
    list_filter = ['name', 'price', 'category', 'slug']
    readonly_fields = ['slug']
    raw_id_fields = ['category']