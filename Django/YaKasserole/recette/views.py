from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.decorators import login_required

from decimal import Decimal

from . forms import *

@login_required
def ajout_recette(request):
    form = AddRecette()
    if request.method == 'POST':
        form = AddRecette(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'recette/ajoutrecette.html', {'form': form});
