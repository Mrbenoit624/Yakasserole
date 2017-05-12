from django import forms
from django.atelier import models
from django.contrib.auth.models import User

class SubscribeAtelier(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SubscribeAtelier, self).__init__(*args, **kwargs)
        self.fields['participants'] = forms.MultipleChoiceField(
                choices=[(o.id, str(o)) for o in auth.User.objects.all()])
        #FIXME: Filter the basic & premium users
        self.fields['participants'].widget.attrs['class'] = 'form-control'

class CreateAtelier(modelForm):
    class Meta:
        model = Atelier

    def __init__(self, *args, **kwargs):
        super(CreateAtelier, self).__init__(*args, **kwargs)
        #FIXME: Filter the chefs
        self.fields['Chef'] = forms.ChoiceField(
                choices=[(o.id, str(o)) for o in auth.User.objects.all()])
        self.fields['nom'].widget.attrs['class'] = 'form-control'
        self.fields['date_inscription'].widget.attrs['class'] = 'form-control'
        self.fields['date_premium'].widget.attrs['class'] = 'form-control'
        self.fields['places'].widget.attrs['class'] = 'form-control'
        self.fields['messages'].widget.attrs['class'] = 'form-control'
        self.fields['lieux'].widget.attrs['class'] = 'form-control'
        self.fields['themes'].widget.attrs['class'] = 'form-control'
        self.fields['chef'].widget.attrs['class'] = 'form-control'
