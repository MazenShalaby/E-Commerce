from django.contrib import admin

from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderItemInline(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['order_id', 'email', 'first_name', 'last_name', 'paid']
    search_fields = ['order_id', 'email', 'first_name', 'last_name', 'city', 'address', 'postal_code']
    list_filter = ['paid', 'created_at', 'updated_at']