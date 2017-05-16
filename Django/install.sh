#!/bin/bash
set +x
postgres -D $PGDATA -k /tmp&
postback=$!

set -e
project=YaKasserole

if [ -d django ];
then
  cd django && git pull && cd -;
else
  git clone git://github.com/django/django.git
fi

# Install django and his modules
pip install --user -e django/
pip install --user -r REQUIREMENT.txt

#Correct unstable versions
to_modify="$HOME/.local/lib/python3.6/site-packages/payments/models.py"
if [ ! -f "$to_modify" ]; then
  to_modify="/usr/local/lib/python3.6/site-packages/payments/models.py"
fi

sed -r 's/(from )(.*)( import reverse)/\1django.urls\3/' "$to_modify" > /tmp/tmp
cat /tmp/tmp > "$to_modify"

#Setup Users
psql -h localhost postgres -f setup_user.sql

#Install new project if it doesn't exist
if [ ! -d "$project" ]; then
  ~/.local/bin/django-admin startproject "$project"
  cd "$project"
fi

#Install different app
apps=('community' 'recette' 'atelier' 'comptes')
cd "$project"
set +e
find . -name 'migrations' -exec rm -rf {} \;
set -e
for i in "${apps[@]}"; do
  if [ ! -d "$i" ]; then
    python manage.py startapp $i
  fi
done

for i in "${apps[@]}"; do
  python manage.py makemigrations $i
  python manage.py migrate $i
done
python manage.py migrate

#enter admin for user
python manage.py shell < ../group.py

#add default recettes
python manage.py loaddata fixtures/recettes.yaml

kill $postback
