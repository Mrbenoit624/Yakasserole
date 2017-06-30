from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, Permission, User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.test.client import RequestFactory
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from datetime import datetime

from decimal import Decimal
from payments import FraudStatus, PaymentStatus, get_payment_model
from payments.urls import process_data

from atelier.models import inscription_log
from community.models import Commentaire
from recette.models import Recette

from . forms import *
from . models import PaymentLink, Premium
from atelier.models import Atelier, Theme, ateliers_themes
from pprint import pprint

import datetime
from dateutil.relativedelta import relativedelta

def connect(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ConnectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #username = request.POST['email'] Before, next doesnt work
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
              login(request, user)
              return HttpResponse('Login success')
            else:
              return render(request, 'comptes/connect.html', {'form': form,
                                                              'password': 'wrong' })
    else:
      form = ConnectForm()
    return render(request, 'comptes/connect.html', {'form': form})

def is_premium(user):
    return user.groups.filter(name='client premium').exists()

@user_passes_test(is_premium)
def end_premium(request):
    prems = Premium.objects.filter(user=request.user).order_by('-date_fin')
    if prems.exists() and datetime.date.today() >= prems[0].date_fin:
        request.user.groups.clear()
        request.user.groups.add(1)

@user_passes_test(is_premium)
def warn_premium(request):
    prems = Premium.objects.filter(user=request.user).order_by('-date_fin')
    #if prems.exists() and datetime.date.today() >= (prems[0].date_fin - relativedelta(days=10)):
        #warn here

@login_required
def profile(request):
    end_premium(request)
    warn_premium(request)
    ateliers = len(inscription_log.objects.filter(user=request.user))
    recettes = len(Recette.objects.filter(user=request.user.id))
    commentaires = len(Commentaire.objects.filter(user=request.user))
    nb_recettes = len(Recette.objects.all())
    nb_inscription = len(inscription_log.objects.all())
    nb_atelier = len(Atelier.objects.all())
    if request.user.is_authenticated:
        return HttpResponse(render(request, 'registration/account.html',
            {'nb_atelier': ateliers,
             'nb_recettes': recettes,
             'nb_commentaires':commentaires,
             'unpaid': len(PaymentLink.objects.filter(user=request.user,
                 payment__status__startswith='WAITING')),
             'user': User.objects.get(pk=request.user.id),
             'nb_recettes_admin': nb_recettes,
             'nb_inscription': nb_inscription,
             'nb_atelier': nb_atelier,
             'now': datetime.datetime.now()
             }));
    else:
        return HttpResponse('Vous avez fait une erreur dans votre connexion');

@login_required
def public_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    if user.groups.filter(name__in=['client', 'client premium']).exists()\
    and request.user.has_perm('auth.cp_clt')\
    or user.groups.filter(name__in=['Responsable des ateliers',\
    'Responsable des utilisateurs']).exists() and request.user.has_perm('auth.cp_resp')\
    or user.groups.filter(name='Chef cuisinier') and request.user.has_perm('auth.cp_chef')\
    or user.is_superuser and request.user.has_perm('auth.cp_admin'):
        ateliers = len(inscription_log.objects.filter(user=user_id))
        recettes = len(Recette.objects.filter(user=user_id))
        commentaires = len(Commentaire.objects.filter(user=user_id))
        themes = None
        if user.groups.filter(name='Chef cuisinier').exists() and request.user.has_perm('auth.cp_chef'):
            ateliers_qs = Atelier.objects.filter(Chef=user.id)
            a_t = ateliers_themes.objects.filter(id=ateliers_qs.values('id'))
            themes = Theme.objects.filter(ateliers_themes__in=a_t)
        if request.user.is_authenticated:
            return HttpResponse(render(request, 'registration/account.html',
                {'nb_atelier': ateliers,
                 'nb_recettes': recettes,
                 'nb_commentaires':commentaires,
                 'unpaid': len(PaymentLink.objects.filter(user=request.user,
                     payment__status__startswith='WAITING')),
                 'user': user,
                 'themes': themes
                 }));
    return redirect('profile');

def inscription(request):
    form = InscriptionForm()
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                    username = form.cleaned_data['username'],
                    email = form.cleaned_data['username'],
                    password = form.cleaned_data['password'],
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name']
                    )
            group = Group.objects.get(name='client')
            group.user_set.add(user)
            login(request, user)
            return profile(request)
    return render(request, 'registration/register.html', {'form': form});

@login_required
def payment(request):
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            Payment = get_payment_model()
            payment = Payment.objects.create(
                    variant='default',  # this is the variant from PAYMENT_VARIANTS
                    description= form.cleaned_data['description'],
                    total= form.cleaned_data['total'],
                    tax= form.cleaned_data['total'] * Decimal(1.2),
                    currency='USD',
                    delivery= form.cleaned_data['delivery'],
                    billing_first_name= form.cleaned_data['billing_first_name'],
                    billing_last_name= form.cleaned_data['billing_last_name'],
                    billing_address_1= form.cleaned_data['billing_address_1'],
                    billing_address_2='',
                    billing_city= form.cleaned_data['billing_city'],
                    billing_postcode= form.cleaned_data['billing_postcode'],
                    billing_country_code= form.cleaned_data['billing_country_code'],
                    billing_country_area= form.cleaned_data['billing_country_area'],
                    customer_ip_address=request.META.get('REMOTE_ADDR'))
            payment.change_status(PaymentStatus.PREAUTH, "only god")
            payment.capture()
            return redirect(process_data, token = payment.token)
            #return HttpResponse(render(request,
            #    'comptes/payments/process/'+ payment.token, {}))
            return payment_details(request, payment.id)
            return HttpResponse('Paiement Enregistré')
    return HttpResponse(render(request, 'comptes/payment.html', {'form': form}))

@login_required
def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'comptes/payments.html', {'form': form,
        'payment': payment, 'post': payment_id})

@login_required
def payment_process(request, process_id):
    form = CardPayment(payment_link=process_id)
    if request.method == 'POST':
        # Shouldn't you pass payment_link here as well?
        form = CardPayment(request.POST)
        if form.is_valid():
            paymentlink = PaymentLink.objects.get(id=form.cleaned_data['id_paymentlink'])
            if paymentlink.user == request.user:
                payment = paymentlink.payment
                if (not payment.status == PaymentStatus.CONFIRMED):
                    payment.change_status(PaymentStatus.PREAUTH, "only god")
                    payment.capture()
                    send_email(payment.description, request.user.email)
                    return redirect('/accounts/payments')
    return render(request, 'comptes/payment_process.html', {'form': form})

def is_client(user):
    return user.groups.filter(name='client').exists()

@user_passes_test(is_client)
def devenir_premium(request):
    form = PremiumForm(request.POST or None)
    form.instance.user_id = request.user.id
    form.instance.date_fin = datetime.date.today() + relativedelta(months=1)
    if form.is_valid():
        Payment = get_payment_model()
        payment = Payment.objects.create(
            variant='default',
            # this is the variant from PAYMENT_VARIANTS
            description="Membre Premium",
            total=Decimal(3.99),
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
        link.premium = form.save()
        link.user = request.user
        link.save()
        request.user.groups.clear()
        request.user.groups.add(2)
        return redirect('profile')
    return render(request, 'comptes/premium.html', {'form': form});

class Listpayments(ListView):
    def get_queryset(self):
        return PaymentLink.objects.filter(user_id=self.request.user.id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Listpayments, self).dispatch(*args, **kwargs)

    model = PaymentLink
    exclude = []

def send_email(description, to):
    subject = "Confirmation de " + description
    message = "Votre paiement pour " + description + " est confirmé"
    from_email = "nepasrepondre@yakasserole.fr"
    send_mail(subject, message, from_email, [to])
