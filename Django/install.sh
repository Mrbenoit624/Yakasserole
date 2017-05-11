#!/bin/bash
# if error occur active this one
if false;then
  sudo mkdir /run/postgresql 2> /dev/null
  sudo chown $USER:users /run/postgresql/
  chmod +x /run/postgresql/
  pg_ctl -l /tmp/pg_log start
  ln -s /run/postgresql/.s.PGSQL.5432 /tmp/.s.PGSQL.5432 2> /dev/null
fi
# DONT FORGET TO LAUNCH THE SERVER
#pg_ctl -l /tmp/pg_log start
postgres -D $PGDATA -k /tmp&
postback=$!

set -e
project=YaKasserole

pip install --user psycopg2

if [ -d django ];
then
  cd django && git pull && cd -;
else
  git clone git://github.com/django/django.git
fi


pip install --user -e django/
pip install --user django-secure
pip install --user django-sslserver

apps=('community' 'recette' 'atelier')

if [ ! -d "$project" ]; then
  ~/.local/bin/django-admin startproject "$project"
  cd "$project"
  set +e
  find . -name 'migrations' -exec rm -rf {} \;
  set -e
  for i in "${apps[@]}"; do
    python manage.py startapp $i
  done
fi

set +e
psql -h localhost postgres -f setup_user.sql
set -e

cd "$project"
for i in "${apps[@]}"; do
  python manage.py makemigrations $i
  python manage.py migrate $i
done
python manage.py migrate

#enter admin for user
python manage.py createsuperuser

python manage.py shell < ../group.py

kill $postback
