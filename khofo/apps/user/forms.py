# Django
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Models
from .models import BuyerUserDetails

User = get_user_model()


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control here border-radius',
        'placeholder': _('Username'),
        'maxlength': 30,
        'minlength': 4,
        'required': 'required',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control here border-radius',
        'placeholder': _('E-mail'),
        'maxlength': 60,
        'minlength': 5,
        'pattern': "[^@]+@[^@]+\.[a-zA-Z]{2,20}",
        'required': 'required',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control here border-radius',
        'placeholder': _('Password'),
        'minlength': 8,
        'maxlength': 30,
        'required': 'required',
        'id': 'pass'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class BuyerUserDetailsForm(forms.ModelForm):
    class Meta:
        model = BuyerUserDetails
        fields = ('address', 'region', 'city', 'zip_code', 'country', 'mobile')


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control here border-radius',
        'placeholder': _('Username'),
        'maxlength': 30,
        'minlength': 4,
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control here border-radius',
        'placeholder': _('E-mail'),
        'maxlength': 60,
        'pattern': "[^@]+@[^@]+\.[a-zA-Z]{2,20}",
        'minlength': 6,
    }))

    class Meta:
        model = User
        fields = ('username', 'email')


class AddressUserForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control here border-radius',
        'placeholder': _('Address'),
        'maxlength': 100,
        'minlength': 5,
    }))
    region = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control here border-radius',
        'placeholder': _('Region'),
        'maxlength': 50,
        'minlength': 3,
        'pattern': "^[A-Za-z -]+$",
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control here border-radius',
        'placeholder': _('City'),
        'maxlength': 50,
        'minlength': 3,
        'pattern': "^[A-Za-z -]+$",
    }))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control here border-radius',
        'placeholder': _('Zip Code'),
        'maxlength': 8,
        'minlength': 5,
        'type': 'number',
    }))
    mobile = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control here border-radius',
        'placeholder': _('Mobile'),
        'maxlength': 15,
        'minlength': 9,
    }))

    class Meta:
        model = BuyerUserDetails

        widgets = {
            'country': forms.Select(attrs={'class': 'form-control custom-select border-radius'}),
        }
        fields = ('address', 'country', 'region', 'city', 'zip_code', 'mobile',)
