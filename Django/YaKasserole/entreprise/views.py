
from django.http import HttpResponse
from django.template import loader


def page(request, page):
    template = loader.get_template('html/entreprise/{}.html'.format(page))
    return HttpResponse(template.render({}, request))
