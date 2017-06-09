#!/bin/bash
postgres -D $PGDATA -k /tmp -r .postgres.log&
echo $! > .postgres.pid
#apps=('YaKasserole' 'community' 'recette' 'atelier' 'comptes')
#for i in "${apps[@]}"; do
#  HTTPS=on python YaKasserole/manage.py test "$i"
#done
HTTPS=on python YaKasserole/manage.py test YaKasserole
kill $(cat .postgres.pid)
rm .postgres.pid
