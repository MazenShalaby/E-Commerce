from django import forms

from .models import Order, OrderPayment

# create your forms here.


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'first_name', 'last_name', 'address', 'city', 'postal_code']


class OrderPaymentForm(forms.ModelForm):
    class Meta:
        model = OrderPayment
        fields = ['payment_phone', 'payment_receipt']
    
    def clean_payment_phone(self):
        payment_phone = self.cleaned_data.get('payment_phone')

        if not payment_phone.isdigit():
            raise forms.ValidationError("Payment phone must be digits!")
        
        if len(payment_phone) != 11:
            raise forms.ValidationError("Payment phone must be 11 digits length!")
        
        valid_prefixes = ['010', '011', '012', '015']     
        if not any(payment_phone.startswith(prefix) for prefix in valid_prefixes):
            raise forms.ValidationError("Payment phone must be one of the following prefixes: 010, 011, 012 or 015!")
        
        return payment_phone