from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from .models import Atelier, ateliers_lieux, ateliers_themes, paricipants_atelier
from .forms import *

@login_required
def ajout_atelier(request):
    form = CreateAtelier()
    if request.method == 'POST':
        form = CreateAtelier(request.POST)
        if form.is_valid():
            saved_form = form.save(commit=False)
            saved_form.save()
            for lieu in form.cleaned_data.get('Lieux'):
                atelier_lieu = ateliers_lieux(ateliers=saved_form, lieux=lieu)
                atelier_lieu.save()
            for theme in form.cleaned_data.get('Themes'):
                atelier_theme = ateliers_themes(ateliers=saved_form, themes=theme)
                atelier_theme.save()
            return reponse_ajout(request, saved_form.id)
    return render(request, 'atelier/ajout.html', {'form': form});

def get_atelier_model(atelier_id):
    return Atelier.objects.filter(id=atelier_id)

@login_required
def reponse_ajout(request, atelier_id):
    return HttpResponse(get_object_or_404(get_atelier_model(atelier_id)))

@login_required
def inscription_atelier(request):
    form = SubscribeAtelier()
    if request.method == 'POST':
        form = SubscribeAtelier(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            saved_form = form.save(commit=False)
            saved_form.save()
            for participant in form.cleaned_data.get('participants'):
                participant_atelier = paricipants_atelier(user=participant, inscription_logs=saved_form)
                participant_atelier.save()
            return HttpResponseRedirect('/')
    return render(request, 'atelier/inscription.html', {'form': form});

class AffichageAtelier(DetailView):
    model = Atelier
    exclude = []

class AffichageAteliers(ListView):
    model = Atelier
    exclude = []
