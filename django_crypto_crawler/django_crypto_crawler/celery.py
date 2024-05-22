from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_crypto_crawler.settings')

app = Celery('django_crypto_crawler')



app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = 'amqp://guest:guest@localhost:5672//'

# app.conf.beat_schedule = {
#     'fetch-candle-data-every-hour': {
#         'task': 'app.tasks.fetch_candle_data_periodically',
#         'schedule': crontab(minute=0, hour='*/1'),  # Run every hour
#     },
# }
app.conf.beat_schedule = {
    'fetch-candle-data-every-1-minutes': {
    'task': 'app.tasks.fetch_candle_data_periodically',
    'schedule': crontab(minute='*/1'),  # Run every 5 minutes
},
}



app.autodiscover_tasks()
