from django.contrib.auth.models import Group, Permission
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
if User.objects.filter(username='cuisse.tot@yakasserole.fr').count()==0:
    cuist = User.objects.create_user('cuisse.tot@yakasserole.fr', 'cuistot@yakasserole.fr', 'cuistot1234')
    cuist.first_name = "Cuisse"
    cuist.last_name = "Tot"
    cuist.save()
    print('  cuistot created... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
else:
    print('  cuistot creation skipped... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')


################################# GROUPE ######################################

print('\x1b[1;39m' + '  création de groupes: ' + '\x1b[0m')

client_g, created = Group.objects.get_or_create(name='client')
print('    - client created... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')

pclient_g, created = Group.objects.get_or_create(
        name='client premium')
print('    - client premium created... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')

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

def add_perm(pcodename, pname):
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    ct = ContentType.objects.get(app_label="auth", model="user")
    if Permission.objects.filter(codename=pcodename).count()==0:
        perm = Permission.objects.create(codename=pcodename,
            name=pname,
            content_type=ct)
        print('    - ' + pname + '... ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
        return perm
    else:
        print('    - ' + pname + '... ' + '\x1b[1;31m' + 'SKIP' + '\x1b[0m')
    return None

print('\x1b[1;39m' + '  création des permissions: ' + '\x1b[0m')

#This permission doesn't make much sense
ccc = add_perm('ccc', 'creation de compte client')
cce = add_perm('cce', 'creation de compte employé')
scu = add_perm('scu', 'suppression de compte utilisateurs')
cp_clt = add_perm('cp_clt', 'consultation de profil client')
cp_resp = add_perm('cp_resp', 'consultation de profil responsable')
cp_admin = add_perm('cp_admin', 'consultation de profil admin')
pdc = add_perm('pdc', 'publication de commentaire')
sdc = add_perm('sdc', 'suppression de commentaire')
cpr = add_perm('cpr', 'creation de page recette')
spr = add_perm('spr', 'suppression de page recette')
vv = add_perm('vv', 'visionage de video')
cpa = add_perm('cpa', 'creation de page d\'atelier')
ass = add_perm('ass', 'acces au statistique du site')


########################### GROUPE PERMISSION #################################
def add_permissions_to_all(perm):
    global client_g
    global pclient_g
    global rda_g
    global rdu_g
    global chef_g
    client_g.permissions.add(perm)
    pclient_g.permissions.add(perm)
    rda_g.permissions.add(perm)
    rdu_g.permissions.add(perm)
    chef_g.permissions.add(perm)

def add_permissions(perm, groups):
    for g in groups:
        g.permissions.add(perm)

if ccc is not None:
    rdu_g.permissions.add(ccc)

if cce is not None:
    rdu_g.permissions.add(cce)

if scu is not None:
    rdu_g.permissions.add(scu)

if cp_clt is not None:
    add_permissions_to_all(cp_clt)

if cp_resp is not None:
    add_permissions(cp_resp, [rda_g, rdu_g, chef_g])
#if cp_admin is not None:
#if pdc is not None:
#if sdc is not None:

if cpr is not None:
    add_permissions_to_all(cpr)

#if spr is not None:

if vv is not None:
    pclient_g.permissions.add(cpr)

if cpa is not None:
    rda_g.permissions.add(cpr)

#if ass is not None:

############################# ADDING TO GROUPS ################################
if cuist:
    chef_g.user_set.add(cuist)
