from django import forms
import recette
import atelier

class SearchFilters(forms.Form):
    t_choices = (('r', 'recettes'),
                 ('a', 'ateliers'),
                 ('p', 'profils'),)
    type = forms.MultipleChoiceField(choices=t_choices, widget=forms.CheckboxSelectMultiple())
    q = forms.CharField(label='Mots-clés', required=False)

    def __init__(self, *args, **kwargs):
        super(SearchFilters, self).__init__(*args, **kwargs)
        self.fields['q'].widget.attrs['class'] = 'form-control'

class RecetteFilters(forms.Form):
    r_type = forms.ModelMultipleChoiceField(queryset=recette.models.Type.objects.all(),
            label='Types de recette', required=False)

    def __init__(self, *args, **kwargs):
        super(RecetteFilters, self).__init__(*args, **kwargs)
        self.fields['r_type'].widget.attrs['class'] = 'form-control'

class AtelierFilters(forms.Form):
    a_theme = forms.ModelMultipleChoiceField(queryset=atelier.models.Theme.objects.all(),
              label="Thèmes d'atelier", required=False)

    def __init__(self, *args, **kwargs):
        super(AtelierFilters, self).__init__(*args, **kwargs)
        self.fields['a_theme'].widget.attrs['class'] = 'form-control'
