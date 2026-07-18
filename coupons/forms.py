from django import forms

# create your forms here.


class CouponApplyForm(forms.Form):
    code = forms.CharField(required=False)