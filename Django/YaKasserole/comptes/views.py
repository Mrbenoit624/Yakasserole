from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import Group
from django.test.client import RequestFactory
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required

from decimal import Decimal
from payments import get_payment_model
from payments import FraudStatus, PaymentStatus
from payments.urls import process_data

from atelier.models import inscription_log
from recette.models import Recette
from community.models import Commentaire

from . forms import *
from . models import PaymentLink

from pprint import pprint

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

def profile(request):
    ateliers = len(inscription_log.objects.filter(user=request.user.id))
    recettes = len(Recette.objects.filter(user=request.user.id))
    commentaires = len(Commentaire.objects.filter(user=request.user.id))
    if request.user.is_authenticated:
        return HttpResponse(render(request, 'registration/account.html',
            {'nb_atelier': ateliers,
             'nb_recettes': recettes,
             'nb_commentaires':commentaires}));
    else:
        return HttpResponse('Vous avez fait une erreur dans votre connexion');


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


class Listpayments(ListView):
    def get_queryset(self):
        return PaymentLink.objects.filter(user_id=self.request.user.id)

    model = PaymentLink
    exclude = []

@login_required
def payment_process(request, process_id):
    form = CardPayment(payment_link=process_id)
    if request.method == 'POST':
        form = CardPayment(request.POST)
        if form.is_valid():
            paymentlink = PaymentLink.objects.get(id=form.cleaned_data['id_paymentlink'])
            if paymentlink.user == request.user:
                payment = paymentlink.payment
                if (not payment.status == PaymentStatus.CONFIRMED):
                    payment.change_status(PaymentStatus.PREAUTH, "only god")
                    payment.capture()
                    return HttpResponse('Paiement Enregistré')
    return render(request, 'comptes/payment_process.html', {'form': form})
