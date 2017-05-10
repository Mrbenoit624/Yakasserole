import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class ConnectForm(forms.Form):
    username = forms.EmailField(label='Email')
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(ConnectForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

class InscriptionForm(forms.Form):
    #username = forms.CharField(label='Username', max_length=30)
    username = forms.EmailField(label='Email')
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
                if len(password) > 7:
                    return passwordr
                else:
                   raise forms.ValidationError('Ce mot de passe n\'est pas sécurisé.')
        raise forms.ValidationError('La confirmation de mot de passe n\' est pas la même.')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Ce login est déjà utilisé.')

#    def clean_email(self):
#        email = self.cleaned_data['email']
#        try:
#            User.objects.get(email=email)
#        except ObjectDoesNotExist:
#            return email
#        raise forms.ValidationError('cet email est déjà utilisé.')

    def __init__(self, *args, **kwargs):
        super(InscriptionForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
#        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['passwordr'].widget.attrs['class'] = 'form-control'
