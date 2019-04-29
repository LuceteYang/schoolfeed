#!/bin/bash

set +e 
echo "==> Django setup, executing: migrate pro"
python  manage.py migrate --settings=config.settings.production
echo "==> Django setup, executing: collectstatic"
python  manage.py collectstatic --settings=config.settings.production

gunicorn -b 0.0.0.0:8004 --env DJANGO_SETTINGS_MODULE=config.settings.production schoolfeed.wsgi:application