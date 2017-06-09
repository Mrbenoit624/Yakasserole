from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth.models import Group, Permission, User
from django.db.models import Q

from atelier.models import Atelier
from recette.models import Recette
from .forms import SearchFilters, RecetteFilters, AtelierFilters

@login_required
def search(request):
    form = SearchFilters()
    rform = RecetteFilters()
    aform = AtelierFilters()
    keywords = request.GET.get('q', '')
    types = request.GET.getlist('type', '')
    r_types = request.GET.getlist('r_type', '')
    a_themes = request.GET.getlist('a_theme', '')

    d_a = len(types) == 0 or 'a' in types
    d_r = len(types) == 0 or 'r' in types
    d_u = len(types) == 0 or 'p' in types

    ateliers = None
    if d_a:
        if len(a_themes):
            ateliers = Atelier.objects.filter(Nom__icontains=keywords, Themes__in=a_themes)
        else:
            ateliers = Atelier.objects.filter(Nom__icontains=keywords)
    recettes = None
    if d_r:
        if len(r_types):
            recettes = Recette.objects.filter(Titre__icontains=keywords, Type__in=r_types)
        else:
            recettes = Recette.objects.filter(Titre__icontains=keywords)
    groups = []
    if request.user.has_perm('auth.cp_clt'):
        groups.extend(['client', 'client premium'])
    if request.user.has_perm('auth.cp_resp'):
        groups.extend(['Responsable des ateliers', 'Responsable des utilisateurs',\
                        'Chef cuisinier'])
    su = request.user.has_perm('auth.cp_admin')

    users = None
    if su:
        users = User.objects.filter(Q(first_name__icontains=keywords)\
                | Q(last_name__icontains=keywords)).order_by('groups') if d_u else None
    else:
        users = User.objects.filter(Q(first_name__icontains=keywords)\
                | Q(last_name__icontains=keywords), groups__name__in=groups,\
                is_superuser=False).order_by('groups') if d_u else None

    return render(request, 'entreprise/search.html',
            { 'ateliers' : ateliers,
              'recettes' : recettes,
              'users' : users,
              'form' : form,
              'rform' : rform,
              'aform' : aform,})
