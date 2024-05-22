from celery import shared_task
from django.core.management import call_command




@shared_task
def fetch_candle_data_periodically():
    call_command('fetch_candle_data')
    

