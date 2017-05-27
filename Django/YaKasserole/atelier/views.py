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
from django.utils import timezone
import datetime
from django.forms.formsets import formset_factory

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from recette.forms import AddComment
from .models import *
from .forms import AddParticipant, SubscribeAtelier, CreateAtelier

@permission_required('auth.cpa')
def ajout_atelier(request):
    form = CreateAtelier()
    if request.method == 'POST':
        form = CreateAtelier(request.POST, request.FILES)
        if form.is_valid():
            saved_form = form.save(commit=False)
            saved_form.save()
            for lieu in form.cleaned_data.get('Lieux'):
                atelier_lieu = ateliers_lieux(ateliers=saved_form, lieux=lieu)
                atelier_lieu.save()
            for theme in form.cleaned_data.get('Themes'):
                atelier_theme = ateliers_themes(ateliers=saved_form, themes=theme)
                atelier_theme.save()

            return HttpResponseRedirect('/atelier/ateliers/' + str(saved_form.id))
    return render(request, 'atelier/ajout.html', {'form': form});

@permission_required('auth.cpa')
def modifier_atelier(request, pk):
    atelier = get_object_or_404(Atelier, id=pk)
    form = CreateAtelier(instance=atelier)
    if request.method == 'POST':
        form = CreateAtelier(request.POST, request.FILES, instance=atelier)
        if form.is_valid():
            saved_form = form.update(commit=False)
            saved_form.update()
            for lieu in form.cleaned_data.get('Lieux'):
                atelier_lieu = ateliers_lieux(ateliers=saved_form, lieux=lieu)
                atelier_lieu.update()
            for theme in form.cleaned_data.get('Themes'):
                atelier_theme = ateliers_themes(ateliers=saved_form, themes=theme)
                atelier_theme.update()

            return HttpResponseRedirect('/atelier/ateliers/' + str(saved_form.id))
    return render(request, 'atelier/modification.html', {'form': form});

def get_atelier_model(atelier_id):
    return Atelier.objects.filter(id=atelier_id)

@login_required
def reponse_ajout(request, atelier_id):
    return HttpResponse(get_object_or_404(get_atelier_model(atelier_id)))

@login_required
def inscription_atelier(request):
    form = SubscribeAtelier()

    ParticipantsFormSet = formset_factory(AddParticipant, min_num=0, max_num=4, extra=0)
    participants_formset = ParticipantsFormSet()

    if request.method == 'POST':
        form = SubscribeAtelier(request.POST)
        form.instance.user = request.user
        participants_formset = ParticipantsFormSet(request.POST)

        done = False
        valid = True
        for p_f in participants_formset:
            if not(p_f.is_valid()) and not(done):
                done = True
            elif done:
                valid = False

        if form.is_valid() and valid:
            atelier_id = form.cleaned_data.get('atelier').pk
            atelier = get_object_or_404(Atelier, id=atelier_id)
            places = atelier.Places - inscription_log.objects.filter(atelier=atelier).count()
            if places > 0:
                saved_form = form.save(commit=False)
                saved_form.save()
                for participant_form in participants_formset:
                    if participant_form.is_valid():
                        participant_save = participant_form.save()
                        p = participants_atelier(
                                participant=participant_save,
                                inscription_logs=saved_form)
                        p.save()

                return HttpResponseRedirect('/atelier/ateliers/' + str(atelier_id))
    return render(request, 'atelier/inscription.html', {'form': form,'participants_formset' : participants_formset});


@login_required
def affichage_atelier(request, pk):
    atelier = get_object_or_404(Atelier, id=pk)
    form = AddComment()
    if request.method == 'POST':
        form = AddComment(request.POST)
        form.instance.user = request.user

        if form.is_valid():
            saved_comment = form.save()
            a_c = ateliers_commentaires(ateliers=atelier, commentaires=saved_comment)
            a_c.save()

    return render(request, 'atelier/atelier_detail.html', { 'form': form, 'object': atelier })

class AffichageAtelier(DetailView):
    model = Atelier
    exclude = []

class AffichageAteliers(ListView):
    def get_queryset(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        if self.request.user.groups.filter(name='client').exists():
            return Atelier.objects.filter(Date_inscription__gte = now, date_atelier__gte = now)
        elif self.request.user.groups.filter(name='pclient').exists():
            return Atelier.objects.filter(Date_premium__gte = now, date_atelier__gte = now)
        return Atelier.objects.filter(date_atelier__gte = now)

    model = Atelier
    exclude = []
