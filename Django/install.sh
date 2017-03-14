#!/bin/bash
# if error occur active this one
if false;then
  sudo mkdir /run/postgresql
  sudo chown $USER:users /run/postgresql/
  chmod +x /run/postgresql/
  pg_ctl -l /tmp/pg_log start
  ln -s /run/postgresql/.s.PGSQL.5432 /tmp/.s.PGSQL.5432
fi
# DONT FORGET TO LAUNCH THE SERVER
pg_ctl -l /tmp/pg_log start

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

if [ ! -d "$project" ]; then
  ~/.local/bin/django-admin startproject "$project"
  cd "$project"
  python manage.py startapp polls
fi

set +e
psql postgres -f setup_user.sql
set -e

cd "$project"
python manage.py makemigrations polls
python manage.py sqlmigrate polls 0001
python manage.py migrate

#enter admin for user 
python manage.py createsuperuser
killall /usr/bin/postgres
