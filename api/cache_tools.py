from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from MegaMarket.settings import CATEGORY_INDICATOR, SUB_CATEGORY_INDICATOR, ITEM_INDICATOR, ALL_INDICATOR
from mega_market_core.models import CHART_DATE_FORMAT_FOR_DATETIME


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def set_one_day_data_to_cache(earned_this_date,
                              bought_this_date,
                              sold_this_date,
                              filter_data,
                              day,
                              time_to_live = CACHE_TTL):

    cache_key = generate_cache_key(filter_data, day)
    data_to_cache = {
        "earned_report_chart": earned_this_date,
        "bought_report_chart": bought_this_date,
        "sold_report_chart": sold_this_date,
    }
    cache.set(cache_key, data_to_cache, time_to_live)


def generate_cache_key(filters, day):
    '''

    :param filters: The standard MegaMarket filter dictionary using the Django ORM .filter sintaxis
    :param day: The day were the data was taken. Either in datatime or string using '%Y-%m-%d' format
    :return: A string with the cache key
            'date_type of category indicator(C, S or I)_id of type or X for all_geo id_target user id'
    '''

    if filters.get('item__sub_category__category_id') is not None:
        category_subcategory_item_indicator = CATEGORY_INDICATOR
        category_subcategory_item_id = str(filters.get('item__sub_category__category_id'))
    elif filters.get('item__sub_category_id') is not None:
        category_subcategory_item_indicator = SUB_CATEGORY_INDICATOR
        category_subcategory_item_id = str(filters.get('item__sub_category_id'))
    elif filters.get('item_id') is not None:
        category_subcategory_item_indicator = ITEM_INDICATOR
        category_subcategory_item_id = str(filters.get('item_id'))
    else:
        category_subcategory_item_indicator = ALL_INDICATOR
        category_subcategory_item_id = ALL_INDICATOR

    if filters.get('geo_id') is not None:
        geo_id = str(filters.get('geo_id'))
    else:
        geo_id = ALL_INDICATOR

    if filters.get('target_user_id') is not None:
        target_user_id = str(filters.get('target_user_id'))
    else:
        target_user_id = ALL_INDICATOR

    if isinstance(day, str) == False:
        if isinstance(day, datetime) == True:
            day = day.strftime(CHART_DATE_FORMAT_FOR_DATETIME)
        else:
            return 'DAY_FORMAT_ERROR'
    cache_key = day + '_' + \
                category_subcategory_item_indicator + '_' + \
                category_subcategory_item_id + '_' + \
                geo_id + '_' + \
                target_user_id
    return cache_key
