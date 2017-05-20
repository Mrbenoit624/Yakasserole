from django import forms
from .models import Atelier, inscription_log
from django.forms import ModelForm
from django.contrib.auth.models import User

class SubscribeAtelier(ModelForm):
    class Meta:
        model = inscription_log
        exclude = ['user', 'Date']

    def __init__(self, *args, **kwargs):
        super(SubscribeAtelier, self).__init__(*args, **kwargs)
        self.fields['participants'].queryset = User.objects.filter(groups__name__in=['client', 'premium'])
        self.fields['atelier'].widget.attrs['class'] = 'form-control'
        self.fields['participants'].widget.attrs['class'] = 'form-control'

class CreateAtelier(ModelForm):
    class Meta:
        model = Atelier
        exclude = ['Commentaires']

    def __init__(self, *args, **kwargs):
        super(CreateAtelier, self).__init__(*args, **kwargs)
        self.fields['Chef'].queryset = User.objects.filter(groups__name='Chef cuisinier')
        self.fields['Nom'].widget.attrs['class'] = 'form-control'
        self.fields['Date_inscription'].widget.attrs['class'] = 'form-control'
        self.fields['Date_premium'].widget.attrs['class'] = 'form-control'
        self.fields['Places'].widget.attrs['class'] = 'form-control'
        self.fields['Messages'].widget.attrs['class'] = 'form-control'
        self.fields['Lieux'].widget.attrs['class'] = 'form-control'
        self.fields['Themes'].widget.attrs['class'] = 'form-control'
        self.fields['Chef'].widget.attrs['class'] = 'form-control'
