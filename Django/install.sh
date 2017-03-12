#!/bin/bash
set -e
pip install --user psycopg2
if [ -d django ];
then
  cd django && git pull && cd -;
else
  git clone git://github.com/django/django.git
fi
pip install --user -e django/
~/.local/bin/django-admin startproject YaKasserole
