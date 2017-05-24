from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory
from django.utils import timezone

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from . models import recettes_ustensiles, recettes_electromenager, recettes_ingredients, recettes_etapes, Recette

from . forms import *

@permission_required('auth.cpr')
def ajout_recette(request):
    form = AddRecette()
    EtapesFormSet = formset_factory(AddEtape, min_num=1, extra=0)
    etapes_formset = EtapesFormSet()
    if request.method == 'POST':
        form = AddRecette(request.POST)
        form.instance.user = request.user
        etapes_formset = EtapesFormSet(request.POST)
        if form.is_valid() and etapes_formset.is_valid():

            recette_save = form.save(commit=False)
            recette_save.save()

            for etape_form in etapes_formset:
                etape_save = etape_form.save()
                r_e = recettes_etapes(recettes=recette_save, etapes=etape_save)
                r_e.save()

            for ustensile in form.cleaned_data.get('Ustensiles'):
                r_u = recettes_ustensiles(recettes=recette_save, ustensiles=ustensile)
                r_u.save()
            for electro in form.cleaned_data.get('Electromenager'):
                r_e = recettes_electromenager(recettes=recette_save, electromenagers=electro)
                r_e.save()
            for ingredient in form.cleaned_data.get('Ingredients'):
                r_i = recettes_ingredients(recettes=recette_save, ingredients=ingredient)
                r_i.save()

            return HttpResponseRedirect('/recette/recettes')
    return render(request, 'recette/ajout.html', {'form': form,
        'etapes_formset' : etapes_formset});

class AffichageRecette(DetailView):
    model = Recette
    exclude = []

class AffichageRecettes(ListView):
    model = Recette
    exclude = []
