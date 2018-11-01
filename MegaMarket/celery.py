import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MegaMarket.settings')

app = Celery('MegaMarket')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'mega_market_core.tasks.create_random_user_accounts',
        'schedule': 30.0,
    },
}
app.conf.timezone = 'UTC'