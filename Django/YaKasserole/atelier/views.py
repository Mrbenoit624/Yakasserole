from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from django.contrib.auth.decorators import login_required

from . forms import *

@login_required
def ajout_atelier(request):
    form = CreateAtelier()
    if request.method == 'POST':
        form = CreateAtelier(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'atelier/ajout.html', {'form': form});

def inscription_atelier(request):
    form = SubscribeAtelier()
    if request.method == 'POST':
        form = SubscribeAtelier(request.POST)
        if form.is_valid():
            form.user = request.user.id
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'atelier/inscription.html', {'form': form});
