from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.contrib.auth.decorators import login_required

from .models import Atelier
from .forms import *

@login_required
def ajout_atelier(request):
    form = CreateAtelier()
    if request.method == 'POST':
        form = CreateAtelier(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'atelier/ajout.html', {'form': form});

@login_required
def inscription_atelier(request):
    form = SubscribeAtelier()
    if request.method == 'POST':
        form = SubscribeAtelier(request.POST)
        if form.is_valid():
            form.user = request.user.id
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'atelier/inscription.html', {'form': form});

class AffichageAtelier(DetailView):
    model = Atelier
    exclude = []

class AffichageAteliers(ListView):
    model = Atelier
    exclude = []
