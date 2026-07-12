from django.contrib import admin

from .models import Account

# Register your models here.


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'age', 'gender', 'is_active', 'date_joined', 'last_login']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['age', 'gender', 'is_active']