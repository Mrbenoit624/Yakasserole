#!/bin/bash
postgres -D $PGDATA -k /tmp -r .postgres.log&
echo $! > .postgres.pid
python YaKasserole/manage.py runsslserver 8080
kill $(cat .postgres.pid)
rm .postgres.pid
