from django import forms
from django.forms import ModelForm
from .models import Recette, Etape
from django.contrib.auth.models import User

class AddRecette(ModelForm):
    class Meta:
        model = Recette
        exclude = ['Etapes', 'Commentaires', 'Date', 'user']

    def __init__(self, *args, **kwargs):
        super(AddRecette, self).__init__(*args, **kwargs)
        self.fields['Titre'].widget.attrs['class'] = 'form-control'
        self.fields['Type'].widget.attrs['class'] = 'form-control'
        #self.fields['Temps_preparation'].widget = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
        self.fields['Temps_preparation'].widget.attrs['class'] = 'form-control'
        self.fields['Temps_cuisson'].widget.attrs['class'] = 'form-control'
        self.fields['Ustensiles'].widget.attrs['class'] = 'form-control'
        self.fields['Electromenager'].widget.attrs['class'] = 'form-control'
        self.fields['Nombre_portions'].widget.attrs['class'] = 'form-control'
        self.fields['Difficulte'].widget.attrs['class'] = 'form-control'
        self.fields['Cout'].widget.attrs['class'] = 'form-control'
        self.fields['Ingredients'].widget.attrs['class'] = 'form-control'
        self.fields['Remarques'].widget.attrs['class'] = 'form-control'

class AddEtape(ModelForm):
    class Meta:
        model = Etape
        fields = ['Titre', 'Contenu']

    def __init__(self, *args, **kwargs):
        super(AddEtape, self).__init__(*args, **kwargs)
        self.fields['Titre'].widget.attrs['class'] = 'form-control'
        self.fields['Contenu'].widget.attrs['class'] = 'form-control'
