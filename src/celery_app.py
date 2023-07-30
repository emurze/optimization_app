# import logging
# from time import sleep
import os

from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

# lg = logging.getLogger(__name__)
#
#
# @app.task
# def debug_task():
#     lg.warning('Hello from debug_task!')
#     sleep(20)
#     lg.info('Hello from debug_task!')
