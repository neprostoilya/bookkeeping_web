#! /bin/bash
source ./venv/Scripts/activate
python manage.py collectstatic --no-input
python manage.py migrate --no-input
exec gunicorn -c ./bin/ginicorn_config.py conf.wsgi

