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

class CreateAtelier(forms.Form):
    nom = forms.CharField(max_length=100)
    date_inscription = forms.DateTimeField(default=timezone.now)
    date_premium = forms.DateTimeField(default=timezone.now)
    places = forms.PositiveIntegerField(default=0)
    messages = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(CreateAtelier, self).__init__(*args, **kwargs)
        self.fields['lieux'] = forms.MultipleChoiceField(
                choices=[(o.id, str(o)) for o in Lieu.objects.all()])
        self.fields['themes'] = forms.MultipleChoiceField(
                choices=[(o.id, str(o)) for o in Theme.objects.all()])
        #FIXME: Filter the chefs
        self.fields['chef'] = forms.ChoiceField(
                choices=[(o.id, str(o)) for o in auth.User.objects.all()])
        self.fields['nom'].widget.attrs['class'] = 'form-control'
        self.fields['date_inscription'].widget.attrs['class'] = 'form-control'
        self.fields['date_premium'].widget.attrs['class'] = 'form-control'
        self.fields['places'].widget.attrs['class'] = 'form-control'
        self.fields['messages'].widget.attrs['class'] = 'form-control'
        self.fields['lieux'].widget.attrs['class'] = 'form-control'
        self.fields['themes'].widget.attrs['class'] = 'form-control'
        self.fields['chef'].widget.attrs['class'] = 'form-control'
