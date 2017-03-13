
from django.http import HttpResponse
from django.template import loader
from django.http import Http404


def page(request, page):
    try:
        template = loader.get_template('entreprise/{}.html'.format(page))
        return HttpResponse(template.render({}, request))
    except:
        raise Http404('Page not found {}'.format(page))
