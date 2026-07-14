from django import forms

# create your forms here.


QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

class CartAddForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())