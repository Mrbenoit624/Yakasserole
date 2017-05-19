from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import Group
from django.test.client import RequestFactory

from decimal import Decimal
from payments import get_payment_model
from payments import FraudStatus, PaymentStatus
from payments.urls import process_data

from . forms import *

from pprint import pprint

def connect(request):
    # if this is a POST request we need to process the form data
    print("email:")
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
    if request.user.is_authenticated:
        return HttpResponse(render(request, 'registration/account.html', {}));
    else:
        return HttpResponse('Vous avez fait une erreur dans votre connexion');


def inscription(request):
    form = InscriptionForm()
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                    username = form.cleaned_data['username'],
                    password = form.cleaned_data['password'],
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name']
                    )
            group = Group.objects.get(name='client')
            group.user_set.add(user)
            login(request, user)
            return profile(request)
    return render(request, 'registration/register.html', {'form': form});

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
            print(payment)
            print(payment)
            print(payment)
            payment.change_status(PaymentStatus.PREAUTH, "only god")
            payment.capture()
            print(payment)
            return redirect(process_data, token = payment.token)
            #return HttpResponse(render(request,
            #    'comptes/payments/process/'+ payment.token, {}))
            return payment_details(request, payment.id)
            return HttpResponse('Paiement Enregistré')
    return HttpResponse(render(request, 'comptes/payment.html', {'form': form}))

def payment_details(request, payment_id):
    print("Putain pourquoi tu me parles d'iterable merde!!!!!!!")
    print(payment_id)
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    pprint(payment)
    pprint(get_payment_model())
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'comptes/payments.html', {'form': form,
        'payment': payment, 'post': payment_id})
