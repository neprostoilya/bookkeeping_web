#! /bin/bash
source /var/www/bookkeeping_web/venv/bin/activate
python manage.py collectstatic --no-input
python manage.py migrate --no-input
exec gunicorn -c ./bin/ginicorn_config.py conf.wsgi

