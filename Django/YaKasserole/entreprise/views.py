from .forms import ContactForm
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.shortcuts import render, redirect

def page(request, page):
    try:
        template = loader.get_template('entreprise/{}.html'.format(page))
        return HttpResponse(template.render({}, request))
    except:
        raise Http404('Page not found {}'.format(page))

def contact(request):
    form = ContactForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        subject = "[CONTACT] " + form.cleaned_data['sujet']
        from_email = form.cleaned_data['mail']
        to = "yakasserole2017@gmail.com"
        c_file = form.cleaned_data['file']
        mail = EmailMessage(subject, form.cleaned_data['message'], from_email, [to])
        mail.attach(c_file.name, c_file.read(), c_file.content_type)
        mail.send()

        return render(request, 'entreprise/contact.html',
                {'form' : form, 'confirm' : True})
    return render(request, 'entreprise/contact.html', {'form' : form})
