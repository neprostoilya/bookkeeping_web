command = '/bookkeeping_web/venv/bin/gunicorn'
pythonpath = '/bookkeeping_web/'
bind = '0.0.0.0:8000'
workers = 17
raw_evn = 'DJANGO_SETTINGS_MODULE=conf.settings.py'
