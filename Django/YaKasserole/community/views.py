from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth.models import Group, Permission, User
from django.db.models import Q

from atelier.models import Atelier
from recette.models import Recette

@login_required
def search(request):
    keywords = request.GET.get('q', '')
    ateliers = Atelier.objects.filter(Nom__icontains=keywords)
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
                | Q(last_name__icontains=keywords)).order_by('groups')
    else:
        users = User.objects.filter(Q(first_name__icontains=keywords)\
                | Q(last_name__icontains=keywords), groups__name__in=groups,\
                is_superuser=False).order_by('groups')

    return render(request, 'entreprise/search.html',
            { 'ateliers' : ateliers,
              'recettes' : recettes,
              'users' : users})
