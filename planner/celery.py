from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planner.settings')

# create a Celery instance and configure it using the settings from Django
app = Celery('planner')

# load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
app.autodiscover_tasks()