from django import forms
from django.forms import ModelForm
from .models import Recette, Etape
from django.contrib.auth.models import User
from community.models import Commentaire

from django.utils.html import mark_safe

class TimePickerWidget(forms.TimeInput):
    def render(self, name, value, attrs=None):
        htmlString = u''
        htmlString += u'<select name="%s">' % (name)
        for i in range(12):
            for j in range(60):
                htmlString += ('<option value="%d:%02d">%dh%02d</option>' % (i,j,i,j))
        htmlString +='</select>'
        return mark_safe(u''.join(htmlString))

class AddRecette(ModelForm):

    class Meta:
        model = Recette
        fields = ['Titre', 'Type', 'Ustensiles', 'Electromenager',
                'Nombre_portions', 'Difficulte', 'Cout', 'Ingredients',
                'Remarques', 'Temps_preparation', 'Temps_cuisson']

    def __init__(self, *args, **kwargs):
        super(AddRecette, self).__init__(*args, **kwargs)
        self.fields['Titre'].widget.attrs['class'] = 'form-control'
        self.fields['Type'].widget.attrs['class'] = 'form-control'
        self.fields['Temps_preparation'].input_format = '%I:%M %p'
        self.fields['Temps_preparation'].widget = TimePickerWidget(format='%i:%M %p')
        self.fields['Temps_preparation'].widget.attrs['class'] = 'form-control'
        self.fields['Temps_cuisson'].widget.attrs['class'] = 'form-control'
        self.fields['Temps_cuisson'].widget = TimePickerWidget(format='%i:%M %p')
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


class AddComment(ModelForm):
    class Meta:
        model = Commentaire
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(AddComment, self).__init__(*args, **kwargs)
        self.fields['Titre'].widget.attrs['class'] = 'form-control'
        self.fields['Messages'].widget.attrs['class'] = 'form-control'
