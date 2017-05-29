import logging

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
from payments import FraudStatus, PaymentStatus

from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from recette.forms import AddComment

from comptes.models import PaymentLink
from payments import get_payment_model
from decimal import Decimal

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
def supprimer_atelier(request, pk):
    atelier = Atelier.objects.filter(id=pk)
    if atelier.exists():
        atelier.delete()
    return HttpResponseRedirect('/atelier/ateliers')

@permission_required('auth.cpa')
def modifier_atelier(request, pk):
    atelier = get_object_or_404(Atelier, id=pk)
    form = CreateAtelier(request.POST or None, request.FILES or None, instance=atelier)
    if form.is_valid():
        saved_form = form.save(commit=False)
        saved_form.save()

        ateliers_lieux.objects.filter(ateliers=atelier).delete()
        for lieu in form.cleaned_data.get('Lieux'):
            atelier_lieu = ateliers_lieux(ateliers=atelier, lieux=lieu)
            atelier_lieu.save()

        ateliers_themes.objects.filter(ateliers=atelier).delete()
        for theme in form.cleaned_data.get('Themes'):
            atelier_theme = ateliers_themes(ateliers=atelier, themes=theme)
            atelier_theme.save()

        return HttpResponseRedirect('/atelier/ateliers/' + str(atelier.id))
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
    ParticipantsFormSet = formset_factory(AddParticipant, min_num=0, max_num=max_additionnel, extra=min(max_additionnel, 1))
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

            total = 0
            if max_additionnel > 0:
                for participant_form in participants_formset:
                    if participant_form.is_valid() and not participant_form.cleaned_data.get('prenom') is None\
                    and not participant_form.cleaned_data.get('nom') is None and total < max_additionnel:
                        participant_save = participant_form.save()
                        p = participants_atelier(
                            participant=participant_save,
                            inscription_logs=saved_form)
                        p.save()
                        total += 1

            atelier = Atelier.objects.filter(id=atelier_id)[0]
            Payment = get_payment_model()
            payment = Payment.objects.create(
                variant='default',
                # this is the variant from PAYMENT_VARIANTS
                description="Inscription à l'Atelier " + atelier.Nom,
                total= atelier.Prix * (total + 1),
                tax=Decimal(20),
                currency='EUR',
                delivery=Decimal(0),
                billing_first_name=request.user.first_name,
                billing_last_name=request.user.last_name,
                billing_address_1='',
                billing_address_2='',
                billing_city='',
                billing_postcode='',
                billing_country_code='',
                billing_country_area='',
                customer_ip_address=request.META.get('REMOTE_ADDR'))
            payment.save()
            link = PaymentLink()
            link.payment = payment
            link.object_to_pay = form.save()
            link.user = request.user
            link.save()

            return HttpResponseRedirect('/atelier/ateliers/'+atelier_id)
    return render(request, 'atelier/inscription.html', {'form':
        form,'participants_formset' : participants_formset, 'max' : max_additionnel,
        'inscrit': inscrit, 'places': places});

def send_email(description, to):
    subject = "Desinscription à " + description
    message = "Votre désinscription à " + description + " est confirmé"
    from_email = "nepasrepondre@yakasserole.fr"
    send_mail(subject, message, from_email, [to])

@login_required
def desinscription_atelier(request, atelier_id):
    inscription = inscription_log.objects.filter(atelier=atelier_id, user=request.user)
    if inscription.exists():
        payment = PaymentLink.objects.get(object_to_pay=inscription).payment
        payment.refund()
        p_a = participants_atelier.objects.filter(inscription_logs = inscription[0])
        Participant.objects.filter(id__in=p_a).delete()
        inscription.delete()
        send_email(Atelier.objects.filter(id=atelier_id)[0].Nom,\
                request.user.email)
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
