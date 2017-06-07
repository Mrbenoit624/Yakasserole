from django.contrib.auth.decorators import login_required, permission_required
from django.forms import modelformset_factory
from django.forms.formsets import formset_factory
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext, loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import *
from .forms import *

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

            return HttpResponseRedirect('/recette/recettes/' + str(recette_save.id))
    return render(request, 'recette/ajout.html', {'form': form,
        'etapes_formset' : etapes_formset});

@permission_required('auth.cpr')
def modifier_recette(request, pk):
    recette = get_object_or_404(Recette, id=pk)
    if recette.user != request.user and not request.user.has_perm('auth.spr'):
        return HttpResponseRedirect('/recette/recettes/' + pk)
    r_etapes = recettes_etapes.objects.filter(recettes=pk).values_list('etapes', flat=True)
    EtapesFormSet = modelformset_factory(Etape, form = AddEtape, min_num = 1, extra = 0)
    form = AddRecette(request.POST or None, instance=recette)
    etapes_formset = EtapesFormSet(request.POST or None, queryset=Etape.objects.filter(pk__in = r_etapes))

    if form.is_valid() and etapes_formset.is_valid():
        recette_save = form.save(commit=False)
        recette_save.save()

        recettes_etapes.objects.filter(recettes=recette).delete()
        for etape_form in etapes_formset:
            etape_save = etape_form.save()
            r_e = recettes_etapes(recettes=recette, etapes=etape_save)
            r_e.save()

        recettes_ustensiles.objects.filter(recettes=recette).delete()
        for ustensile in form.cleaned_data.get('Ustensiles'):
            r_u = recettes_ustensiles(recettes=recette, ustensiles=ustensile)
            r_u.save()
        recettes_electromenager.objects.filter(recettes=recette).delete()
        for electro in form.cleaned_data.get('Electromenager'):
            r_e = recettes_electromenager(recettes=recette, electromenagers=electro)
            r_e.save()
        recettes_ingredients.objects.filter(recettes=recette).delete()
        for ingredient in form.cleaned_data.get('Ingredients'):
            r_i = recettes_ingredients(recettes=recette, ingredients=ingredient)
            r_i.save()

        return HttpResponseRedirect('/recette/recettes/' + str(recette_save.id))

    return render(request, 'recette/modification.html', {'form': form,
        'etapes_formset' : etapes_formset});

@permission_required('auth.cpr')
def supprimer_recette(request, pk):
    recette = get_object_or_404(Recette, id=pk)
    if (recette.user == request.user or request.user.has_perm('auth.spr')) and recette.exists():
        recette.delete()
    return HttpResponseRedirect('/recette/recettes/' + pk)

@login_required
def affichage_recette(request, pk):
    recette = get_object_or_404(Recette, id=pk)
    form = AddComment()
    own = recette.user == request.user or request.user.has_perm('auth.spr')
    if request.method == 'POST':
        form = AddComment(request.POST)
        form.instance.user = request.user

        if form.is_valid():
            saved_comment = form.save()
            r_c = recettes_commentaires(recettes=recette, commentaires=saved_comment)
            r_c.save()

    return render(request, 'recette/recette_detail.html', { 'form': form, 'object': recette,
        'own': own})

class AffichageRecettes(ListView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AffichageRecettes, self).dispatch(*args, **kwargs)

    model = Recette
    exclude = []
