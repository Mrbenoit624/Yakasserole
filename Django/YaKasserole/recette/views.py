from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from django.contrib.auth.decorators import login_required

from . forms import *

@login_required
def ajout_recette(request):
    form = AddRecette()
    EtapesFormSet = formset_factory(AddEtape, extra=2, min_num=1)
    etapes_formset = EtapesFormSet()
    if request.method == 'POST':
        form = AddRecette(request.POST)
        etapes_formset = EtapesFormSet(request.POST)
        if form.is_valid() and etapes_formset.is_valid():

            recette_save = form.save()
            for etape_form in etapes_formset:
                etape_save = etape_form.save()
                recette_save.Etapes.add(etape_form)

            return HttpResponseRedirect('/')
    return render(request, 'recette/ajout.html', {'form': form,
        'etapes_formset' : etapes_formset});
