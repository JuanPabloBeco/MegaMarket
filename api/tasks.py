from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from datetime import datetime, timedelta, date

import logging

from celery import shared_task
from django.core.cache import cache

from api.serializers import BuySerializerWithTime, SellSerializerWithTime, EarnSerializerWithTime
from mega_market_core.data_generator import INITIAL_AMOUNT, MAX_DAILY_TRANSACTION
from mega_market_core.models import Item, TargetUser, Geo, Buy, Sell, CHART_DATE_FORMAT_FOR_DATETIME

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@shared_task
def cache_opening_charts():
    filter_data = {'date__gt': date.today() - timedelta(days=1), 'date__lt': date.today()}

    bought_serializer = BuySerializerWithTime(data=filter_data)
    bought_serializer.is_valid()
    bought_data = list(bought_serializer.data.get("bought_report_chart"))
    sold_serializer = SellSerializerWithTime(data=filter_data)
    sold_serializer.is_valid()
    sold_data = list(sold_serializer.data.get("sold_report_chart"))
    earned_serializer = EarnSerializerWithTime(data={
        'filter_data': filter_data.copy(),
        'bought_data': bought_data,
        'sold_data': sold_data,
        'send_to_cache': True,
    })
    earned_serializer.is_valid()

    data_to_cache = {
        "earned_report_chart": earned_serializer.data.get("earned_report_chart"),
        "bought_report_chart": bought_data,
        "sold_report_chart": sold_data,
    }

    cache.set(filter_data['date__gt'].strftime(CHART_DATE_FORMAT_FOR_DATETIME), data_to_cache, CACHE_TTL)
