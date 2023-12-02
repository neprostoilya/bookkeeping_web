python manage.py collectstatic --no-input
python manage.py migrate --no-input
exec gunicorn -c /bookkeeping_web/bin/gunicorn_config.py conf.wsgi