from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
from django.forms.widgets import HiddenInput
from django.forms.widgets import SelectDateWidget

from .models import Atelier, inscription_log, Participant

import datetime

class FullNameChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()

class SubscribeAtelier(ModelForm):
    class Meta:
        model = inscription_log
        exclude = ['Date', 'participants']

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id',None)
        self.atelier_id = kwargs.pop('atelier_id',None)
        super(SubscribeAtelier, self).__init__(*args, **kwargs)
        self.fields['atelier'].widget = HiddenInput()
        self.initial['atelier'] = self.atelier_id
        self.fields['user'].widget = HiddenInput()
        self.initial['user'] = self.user_id

class AddParticipant(ModelForm):
    class Meta:
        model = Participant
        exclude = []

    def __init__(self, *args, **kwargs):
        super(AddParticipant, self).__init__(*args, **kwargs)
        self.fields['prenom'].widget.attrs['class'] = 'form-control'
        self.fields['nom'].widget.attrs['class'] = 'form-control'

class CreateAtelier(ModelForm):

    Chef = FullNameChoiceField(queryset = User.objects.filter(groups__name='Chef cuisinier'))
    Date_inscription = forms.DateField(widget=SelectDateWidget())
    Date_premium = forms.DateField(widget=SelectDateWidget())
    date_atelier = forms.DateField(widget=SelectDateWidget())

    class Meta:
        model = Atelier
        exclude = ['Commentaires']

    def clean_Date_premium(self):
        date = self.cleaned_data['Date_premium']
        if date <= datetime.date.today():
            raise forms.ValidationError('La date d\'inscription premium doit-être supérieure à ajourd\'hui', 'd_p')
        return date

    def clean_Date_inscription(self):
        date = self.cleaned_data['Date_inscription']
        if date <= datetime.date.today():
            raise forms.ValidationError('La date d\'inscription doit-être supérieure à ajourd\'hui', 'd_i')
        return date

    def clean_date_atelier(self):
        date_atelier = self.cleaned_data['date_atelier']
        if date_atelier <= datetime.date.today():
            raise forms.ValidationError('La date de l\'atelier doit-être supérieure à ajourd\'hui', 'd_a')
        return date_atelier

    def __init__(self, *args, **kwargs):
        super(CreateAtelier, self).__init__(*args, **kwargs)
        self.fields['Chef'].widget.attrs['class'] = 'form-control'
        self.fields['Prix'].widget.attrs['class'] = 'form-control'
        self.fields['Nom'].widget.attrs['class'] = 'form-control'
        self.fields['Date_inscription'].widget.attrs['class'] = 'form-control'
        self.fields['Date_premium'].widget.attrs['class'] = 'form-control'
        self.fields['date_atelier'].widget.attrs['class'] = 'form-control'
        self.fields['Places'].widget.attrs['class'] = 'form-control'
        self.fields['Messages'].widget.attrs['class'] = 'form-control'
        self.fields['Messages'].label = 'Descriptif'
        self.fields['Lieux'].widget.attrs['class'] = 'form-control'
        self.fields['Themes'].widget.attrs['class'] = 'form-control'
        self.fields['picture'].widget.attrs['class'] = 'form-control'
        self.fields['picture'].label = 'Photo de l\'atelier'
