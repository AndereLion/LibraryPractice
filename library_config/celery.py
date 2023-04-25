import os

from celery import Celery

"""
run celery worker: celery -A library_config worker -l info
run celery beat: celery -A library_config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_config.settings')

app = Celery('library_config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
