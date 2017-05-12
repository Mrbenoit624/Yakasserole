from django import forms
from django.recette import models
from django.contrib.auth.models import User

class AddRecette(modelForm):
    class Meta:
        model = Recette
        exclude = ['Etapes', 'Commentaires', 'Date', 'user_id']

    def __init__(self, *args, **kwargs):
        super(AddRecette, self).__init__(*args, **kwargs)
        self.fields['Titre'].widget.attrs['class'] = 'form-control'
        self.fields['Type_id'].widget.attrs['class'] = 'form-control'
        self.fields['Temps_preparation'].widget.attrs['class'] = 'form-control'
        self.fields['Temps_cuissonp'].widget.attrs['class'] = 'form-control'
        self.fields['Ustensiles'].widget.attrs['class'] = 'form-control'
        self.fields['Electromenager'].widget.attrs['class'] = 'form-control'
        self.fields['Nombre_portions'].widget.attrs['class'] = 'form-control'
        self.fields['Difficulte'].widget.attrs['class'] = 'form-control'
        self.fields['Cout'].widget.attrs['class'] = 'form-control'
        self.fields['Ingredients'].widget.attrs['class'] = 'form-control'
        self.fields['Etapes'].widget.attrs['class'] = 'form-control'
        self.fields['Remarques'].widget.attrs['class'] = 'form-control'

class AddEtape(modelForm):
    class Meta:
        model = Etape
