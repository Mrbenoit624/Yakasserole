from django import forms
from .models import Atelier, inscription_log, Participant
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

class FullNameChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()

class SubscribeAtelier(ModelForm):
    class Meta:
        model = inscription_log
        exclude = ['user', 'Date']

    def __init__(self, *args, **kwargs):
        super(SubscribeAtelier, self).__init__(*args, **kwargs)
        self.fields['atelier'].widget.attrs['class'] = 'form-control'
        self.fields['participants'].widget.attrs['class'] = 'form-control'

class AddParticipant(ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(AddEtape, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'

class CreateAtelier(ModelForm):

    Chef = FullNameChoiceField(queryset = User.objects.filter(groups__name='Chef cuisinier'))

    class Meta:
        model = Atelier
        exclude = ['Commentaires']

    def __init__(self, *args, **kwargs):
        super(CreateAtelier, self).__init__(*args, **kwargs)
        self.fields['Chef'].widget.attrs['class'] = 'form-control'
        self.fields['Nom'].widget.attrs['class'] = 'form-control'
        self.fields['Date_inscription'].widget.attrs['class'] = 'form-control'
        self.fields['Date_premium'].widget.attrs['class'] = 'form-control'
        self.fields['date_atelier'].widget.attrs['class'] = 'form-control'
        self.fields['Places'].widget.attrs['class'] = 'form-control'
        self.fields['Messages'].widget.attrs['class'] = 'form-control'
        self.fields['Lieux'].widget.attrs['class'] = 'form-control'
        self.fields['Themes'].widget.attrs['class'] = 'form-control'
