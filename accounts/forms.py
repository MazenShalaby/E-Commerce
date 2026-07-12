from django import forms

from .models import Account

# create your forms here.


class RegisterForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'age', 'gender', 'profile_picture']
    
    def clean(self):
        cleaned_data = super().clean
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if (password and confirm_password) and (password != confirm_password):
            raise forms.ValidationError("Two passwords don't match!")
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email address'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['age'].widget.attrs['placeholder'] = 'Enter your age'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirm your password'