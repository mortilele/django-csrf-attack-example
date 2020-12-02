#!/usr/bin/env bash
source '../envs/django-csrf-attack-example/bin/activate'
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
