#!/bin/bash
SECRET_KEY=${SECRET_KEY:-paranoid}
ALLOWED_HOSTS=${ALLOWED_HOSTS:-*}
DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-screamshotter.settings}

. /opt/ve/screamshotter/bin/activate

cd /opt/apps/screamshotter
git pull origin master

/usr/local/bin/uwsgi \
    --http-socket 0.0.0.0:8000 \
    -p 4 \
    -b 32768 \
    -T \
    --master \
    --max-requests 5000 \
    -H /opt/ve/screamshotter \
    --module wsgi:application