from django import forms
import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class ConnectForm(forms.Form):
    username = forms.CharField(label='Username', max_length=10)
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

class InscriptionForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Prénom')
    last_name = forms.CharField(label='Nom')
    password = forms.CharField(label='Password',
            widget=forms.PasswordInput())
    passwordr = forms.CharField(label='Password (Retype)',
            widget=forms.PasswordInput())

    def clean_passwordr(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            passwordr = self.cleaned_data['passwordr']
            if password == passwordr:
                return passwordr
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain\
                                alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')
