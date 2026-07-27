from django.contrib import admin

from .models import Cart, CartItem

# Register your models here.


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    
