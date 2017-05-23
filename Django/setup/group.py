from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User;

############################# ADDING USERS ####################################

############################ CREATE SUPER USER ################################

username = "admin"
password = "admin1234"
email = ""

if User.objects.filter(username=username).count()==0:
    user = User.objects.create_superuser(username, email, password)
    user.first_name = "Jean"
    user.last_name = "Roger"
    user.save()
    print('  Superuser created... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('  Superuser creation skipped... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

############################# CUISTOTS ########################################
cuist = None
if User.objects.filter(username=username).count()==0:
    cuist = User.objects.create_user('dummy_cuistot', 'cuistot@yakasserole.fr', 'cuistot1234')
    cuist.first_name = "Cuisse"
    cuist.last_name = "Tot"
    cuist.save()
    print('  cuistot created... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('  cuistot creation skipped... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')


################################# CONTEXT #####################################


ct = ContentType.objects.get(app_label="auth", model="user")

################################# GROUPE ######################################

print('\x1b[1;39m' + '  création de groupes: ' + '\x1b[0m')

client_g, created = Group.objects.get_or_create(name='client')
print('    - client created... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')

rda_g, created = Group.objects.get_or_create(
        name='Responsable des ateliers')
print('    - Responsable des ateliers created... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')

rdu_g, created = Group.objects.get_or_create(
        name='Responsable des utilisateurs')
print('    - Responsable des utilisateurs created... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')

chef_g, created = Group.objects.get_or_create(
        name='Chef cuisinier')
print('    - Chef cuisinier created... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')

############################### PERMISSION ####################################


print('\x1b[1;39m' + '  création des permissions: ' + '\x1b[0m')

if Permission.objects.filter(codename='ccc').count()==0:
    ccc_p = Permission.objects.create(codename='ccc',
        name='creation de compte client',
        content_type=ct)
    rdu_g.permissions.add(ccc_p)
    client_g.permissions.add(ccc_p)
    print('    - creation de compte client... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - creation de compte client... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

if Permission.objects.filter(codename='cce').count()==0:
    cce_p = Permission.objects.create(codename='cce',
        name='creation de compte employé',
        content_type=ct)
    rdu_g.permissions.add(cce_p)
    print('    - creation de compte employé... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - creation de compte employé... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

if Permission.objects.filter(codename='scu').count()==0:
    scu_p = Permission.objects.create(codename='scu',
        name='suppression de compte utilisateurs',
        content_type=ct)
    rdu_g.permissions.add(scu_p)
    client_g.permissions.add(scu_p)
    print('    - supression de compte utilisateurs... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - supression de compte utilisateurs... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

if Permission.objects.filter(codename='cp_clt').count()==0:
    cp_clt_p = Permission.objects.create(codename='cp_clt',
        name='consultation de profil client',
        content_type=ct)
    print('    - consultation de profil client... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - consultation de profil client... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

if Permission.objects.filter(codename='cp_resp').count()==0:
    cp_resp_p = Permission.objects.create(codename='cp_resp',
        name='consultation de profil responsable',
        content_type=ct)
    print('    - consultation de profil responsable... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - consultation de profil responsable... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

if Permission.objects.filter(codename='cp_admin').count()==0:
    cp_admin_p = Permission.objects.create(codename='cp_admin',
        name='consultation de profil admin',
        content_type=ct)
    print('    - consultation de profil admin... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - consultation de profil admin... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

if Permission.objects.filter(codename='pdc').count()==0:
    pdc_p = Permission.objects.create(codename='pdc',
        name='publication de commentaire',
        content_type=ct)
    print('    - publication de commentaire... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - publication de commentaire... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

if Permission.objects.filter(codename='sdc').count()==0:
    sdc_p = Permission.objects.create(codename='sdc',
        name='suppression de commentaire',
        content_type=ct)
    print('    - suppression de commentaire... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - suppression de commentaire... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

if Permission.objects.filter(codename='cpr').count()==0:
    cpr_p = Permission.objects.create(codename='cpr',
        name='creation de page recette',
        content_type=ct)
    print('    - creation de page recette... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - creation de page recette... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

if Permission.objects.filter(codename='spr').count()==0:
    spr_p = Permission.objects.create(codename='spr',
        name='suppression de page recette',
        content_type=ct)
    print('    - suppression de page recette... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - suppression de page recette... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

if Permission.objects.filter(codename='vv').count()==0:
    vv_p = Permission.objects.create(codename='vv',
        name='visionage de video',
        content_type=ct)
    print('    - visionage de video... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - visionage de video... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

if Permission.objects.filter(codename='cpa').count()==0:
    cpa_p = Permission.objects.create(codename='cpa',
        name='creation de page d\'atelier',
        content_type=ct)
    print('    - creation de page d\'atelier... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - creation de page d\'atelier... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')

if Permission.objects.filter(codename='ass').count()==0:
    cpa_p = Permission.objects.create(codename='ass',
        name='acces au statistique du site',
        content_type=ct)
    print('    - acces au statistique du site... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('    - acces au statistique du site... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')



########################### GROUPE PERMISSION #################################


#client_g.permissions.add(client_p)
#rda_g.permissions.add(rda_p)
#rdu_g.permissions.add(rdu_p)
#chef_g.permissions.add(chef_p)

############################# ADDING TO GROUPS ################################
if cuist:
    chef_g.user_set.add(user)
