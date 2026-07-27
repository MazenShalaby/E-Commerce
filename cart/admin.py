from django.contrib import admin

from .models import Cart, CartItem

# Register your models here.


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ['user', 'coupon', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user', 'coupon']
