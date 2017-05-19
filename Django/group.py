from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User;

############################ CREATE SUPER USER ################################

username = "admin"
password = "admin1234"
email = ""

if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');

################################# CONTEXT #####################################


ct = ContentType.objects.get(app_label="auth", model="user")

################################# GROUPE ######################################


client_g, created = Group.objects.get_or_create(name='client')

rda_g, created = Group.objects.get_or_create(
        name='Responsable des ateliers')

rdu_g, created = Group.objects.get_or_create(
        name='Responsable des utilisateurs')

chef_g, created = Group.objects.get_or_create(
        name='Chef cuisinier')

############################### PERMISSION ####################################


client_p = Permission.objects.create(codename='client',
        name='client',
        content_type=ct)

rda_p = Permission.objects.create(codename='rda',
        name='Responsable des ateliers',
        content_type=ct)

rdu_p = Permission.objects.create(codename='rdu',
        name='Responsable des utilisateurs',
        content_type=ct)

chef_p = Permission.objects.create(codename='chef',
        name='Chef cuisinier',
        content_type=ct)

########################### GROUPE PERMISSION #################################


client_g.permissions.add(client_p)
rda_g.permissions.add(rda_p)
rdu_g.permissions.add(rdu_p)
chef_g.permissions.add(chef_p)

