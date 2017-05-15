import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from payments import get_payment_model, RedirectNeeded


class ConnectForm(forms.Form):
    username = forms.EmailField(label='Email')
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(ConnectForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

class InscriptionForm(forms.Form):
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

    def __init__(self, *args, **kwargs):
        super(InscriptionForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['passwordr'].widget.attrs['class'] = 'form-control'


def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'payment.html',
                            {'form': form, 'payment': payment})

def PaymentForm(request):
    description = forms.CharField(label='description')
    total = forms.DecimalField(label='totale')
    tax = forms.DecimalField(label='taxe')
    delivery = forms.DecimalField(label='delivery')
    billing_first_name = forms.CharField(label='prénom')
    billing_last_name = forms.CharField(label='Nom')
    billing_address_1 = forms.CharField(label='Adresse')
    billing_city = forms.CharField(label='Ville')
    billing_postcode = forms.CharField(label='Code Postal')
    billing_country_code = forms.CharField(label='FR')
    billing_country_area = forms.CharField(label='Pays')
