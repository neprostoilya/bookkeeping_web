import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

task = Celery('conf')
task.config_from_object('django.conf:settings', namespace='CELERY')
task.autodiscover_tasks()
