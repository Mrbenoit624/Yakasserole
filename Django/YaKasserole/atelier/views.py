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

def get_place_atelier(atelier_id):
    logs = inscription_log.objects.filter(atelier_id=atelier_id)
    participants = participants_atelier.objects.filter(inscription_logs__in=logs)
    return Atelier.objects.filter(id=atelier_id)[0].Places - logs.count() - participants.count()

@login_required
def reponse_ajout(request, atelier_id):
    return HttpResponse(get_object_or_404(get_atelier_model(atelier_id)))

@login_required
def inscription_atelier(request, atelier_id):
    form = SubscribeAtelier(user_id=request.user.id, atelier_id=atelier_id)

    inscrit = inscription_log.objects.filter(atelier=atelier_id, user=request.user).exists()
    places = get_place_atelier(atelier_id)
    max_additionnel = max(min(4, places - 1), 0)
    if request.user.groups.filter(name='client').exists():
        max_additionnel = 0
    ParticipantsFormSet = formset_factory(AddParticipant, min_num=0, max_num=max_additionnel, extra=1)
    participants_formset = ParticipantsFormSet()

    if request.method == 'POST' and not(inscrit):
        form = SubscribeAtelier(request.POST, user_id=request.user.id,
                atelier_id=atelier_id)
        form.user_id = request.user.id
        participants_formset = ParticipantsFormSet(request.POST)

        if form.is_valid() and (places >= len(participants_formset) + 1):
            form.user = request.user
            saved_form = form.save(commit=False)
            saved_form.save()
            if max_additionnel > 0:
                for participant_form in participants_formset:
                    participant_save = participant_form.save()
                    p = participants_atelier(
                        participant=participant_save,
                        inscription_logs=saved_form)
                    p.save()
            return HttpResponseRedirect('/atelier/ateliers/'+atelier_id)
    return render(request, 'atelier/inscription.html', {'form':
        form,'participants_formset' : participants_formset, 'max' : max_additionnel,
        'inscrit': inscrit, 'places': places});

@login_required
def desinscription_atelier(request, atelier_id):
    inscription = inscription_log.objects.filter(atelier=atelier_id, user=request.user)
    if inscription.exists():
        p_a = participants_atelier.objects.filter(inscription_logs = inscription[0])
        Participant.objects.filter(id__in=p_a).delete()
        inscription.delete()
    return HttpResponseRedirect('/atelier/ateliers/' + atelier_id)

@login_required
def affichage_atelier(request, pk):
    atelier = get_object_or_404(Atelier, id=pk)
    atelier.LastPlaces = get_place_atelier(atelier.id)
    form = AddComment()
    inscrit = inscription_log.objects.filter(atelier=atelier, user=request.user).exists()
    if request.method == 'POST':
        form = AddComment(request.POST)
        form.instance.user = request.user

        if form.is_valid():
            saved_comment = form.save()
            a_c = ateliers_commentaires(ateliers=atelier, commentaires=saved_comment)
            a_c.save()

    return render(request, 'atelier/atelier_detail.html', { 'form': form, 'object': atelier,
        'inscrit': inscrit })

def filter_displayable(request):
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        if request.user.groups.filter(name='client').exists():
            return Atelier.objects.filter(Date_inscription__lte = now, date_atelier__gte = now)
        elif request.user.groups.filter(name='pclient').exists():
            return Atelier.objects.filter(Date_premium__lte = now, date_atelier__gte = now)
        return Atelier.objects.filter(date_atelier__gte = now)

class AffichageAtelier(DetailView):
    def get_queryset(self):
        return filter_displayable(self.request)

    def get_context_data(self, **kwargs):
        context = super(AffichageAtelier, self).get_context_data(**kwargs)
        context['object'].LastPlaces = get_place_atelier(context['object'].id)
        return context

    model = Atelier
    exclude = []

class AffichageAteliers(ListView):
    def get_queryset(self):
        return filter_displayable(self.request)

    model = Atelier
    exclude = []
