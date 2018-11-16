import os
from celery import Celery

REFRESH_INTERVAL_SECONDS = 30
NEW_DATA_INTERVAL_SECONDS = 5
DAILY_OPENING_API_REQUEST_CACHE_INTERVAL_SECONDS = 60 #* 60 * 24 # One day between each yesterday save

ONE_DAY_IN_SECONDS = 60 * 60 * 24

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MegaMarket.settings')

app = Celery('MegaMarket')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'mega_market_core.tasks.create_random_user_accounts',
        'schedule': NEW_DATA_INTERVAL_SECONDS,
    },
    'cache-opening-charts': {
        'task': 'api.tasks.cache_opening_charts',
        'schedule': DAILY_OPENING_API_REQUEST_CACHE_INTERVAL_SECONDS,
    },
    'foreign-exchange-rates-update': {
        'task': 'mega_market_core.foreign_exchange.get_exchange_rate_dictionary',
        'schedule': DAILY_OPENING_API_REQUEST_CACHE_INTERVAL_SECONDS,
    },
}
app.conf.timezone = 'UTC'


