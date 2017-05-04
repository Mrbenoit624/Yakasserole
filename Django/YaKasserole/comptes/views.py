from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import Group
from django.test.client import RequestFactory
from . forms import *

def connect(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ConnectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = request.POST['email']
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
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                    username = form.cleaned_data['username'],
                    password = form.cleaned_data['password'],
                    email = form.cleaned_data['email'],
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name']
                    )
            group = Group.objects.get(name='client')
            group.user_set.add(user)
            login(request, user)
            return profile(request)
    form = InscriptionForm()
    return render(request, 'registration/register.html', {'form': form});
