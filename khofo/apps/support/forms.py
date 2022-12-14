from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Mail


class EmailForm(forms.ModelForm):
    name = forms.CharField(max_length=30, min_length=4,
                           widget=forms.TextInput(attrs={
                               'class': "form-control mb-30l border-radius",
                               'placeholder': _('name'),
                               'required': 'required',
                               'pattern': "^[A-Za-z -]+$",
                           }))
    email = forms.EmailField(max_length=60, min_length=6,
                             widget=forms.EmailInput(attrs={
                                 'class': "form-control mb-30 border-radius",
                                 'id': "clientemail",
                                 'placeholder': _('Email'),
                                 'pattern': "[^@]+@[^@]+\.[a-zA-Z]{2,20}",
                                 'required': 'required',
                             }))
    message = forms.CharField(max_length=1000,
                              widget=forms.Textarea(attrs={
                                  'class': "form-control mb-30 border-radius",
                                  'placeholder': _('Message'),
                                  'required': 'required',
                                  'rows': 5,
                              }))

    # document1 = forms.FileField(widget=forms.FileInput(attrs={'class': "form-control mb-30",}))

    class Meta:
        model = Mail
        fields = (
            'name', 'email', 'message', 'document1', 'document2', 'document3', 'document3', 'document4', 'document5',)
