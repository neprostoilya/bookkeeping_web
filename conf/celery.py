import os

from celery import Celery

from conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery('conf')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()