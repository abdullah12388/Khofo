from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Advertisement


class AdvertisementAddForm(forms.ModelForm):
    advertiserName = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Advertiser Name'),
        'maxlength': 500,
        'id': 'advertiserName',
        'required': 'required',
    }))
    advertiserEmail = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': _('Advertiser Email'),
        'maxlength': 500,
        'id': 'advertiserEmail',
        'required': 'required',
    }))
    advertiserPhone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Advertiser Phone'),
        'maxlength': 100,
        'id': 'advertiserPhone',
        'required': 'required',
    }))
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class': 'form-control',
        'placeholder': _('File'),
        'id': 'image',
        'required': 'required',
    }))
    page = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Page'),
        'maxlength': 100,
        'id': 'page',
        'required': 'required',
    }))
    startDate = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': _('Start Date'),
        'type': 'date',
        'id': 'startDate',
        'required': 'required',
    }))
    endDate = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': _('End Date'),
        'type': 'date',
        'id': 'endDate',
        'required': 'required',
    }))


    class Meta:
        model = Advertisement

        widgets = {
            'duration': forms.Select(attrs={'class': 'form-control','id': 'duration','required': 'required',}),
            'interval': forms.Select(attrs={'class': 'form-control','id': 'interval'}),
        }

        fields = ('advertiserName',
                  'advertiserEmail',
                  'advertiserPhone',
                  'image',
                  'page',
                  'startDate',
                  'endDate',
                  'duration',
                  'interval',)