#!/bin/bash
pg_ctl -l /tmp/pg_log start
python YaKasserole/manage.py runserver 8080
killall /usr/bin/postgres
