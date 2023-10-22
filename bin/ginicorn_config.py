command = './venv/bin/gunicorn'
pythonpath = './bookkeeping_web/'
bind = '127.0.0.1:8000'
workers = 3
raw_evn = 'DJANGO_SETTINGS_MODULE=conf.settings.py'
