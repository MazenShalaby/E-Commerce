from django import forms

from .models import Order

# create your forms here.


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'first_name', 'last_name', 'address', 'city', 'postal_code']
