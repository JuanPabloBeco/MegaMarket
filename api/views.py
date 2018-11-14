from datetime import datetime, timedelta, date
import logging

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.cache_tools import generate_cache_key
from api.serializers import BuySerializer, SellSerializer, EarnSerializer, BuySerializerWithTime, \
    SellSerializerWithTime, EarnSerializerWithTime

from mega_market_core.models import CHART_DATE_FORMAT_FOR_DATETIME, CHART_DATE_FORMAT_FOR_AMCHARTS, \
    CHART_DATETIME_FORMAT_FOR_AMCHARTS

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def get_chart_data(filter_data):  # I had an error when the self wasn't there
    bought_serializer = BuySerializer(data=filter_data)
    bought_serializer.is_valid()
    bought_data = list(bought_serializer.data.get("bought_report_chart"))
    sold_serializer = SellSerializer(data=filter_data)
    sold_serializer.is_valid()
    sold_data = list(sold_serializer.data.get("sold_report_chart"))
    earned_serializer = EarnSerializer(data={
        'filter_data': filter_data.copy(),
        'bought_data': bought_data,
        'sold_data': sold_data,
        'send_to_cache': True,
    })
    earned_serializer.is_valid()
    earned_data = earned_serializer.data.get("earned_report_chart")
    return {
        "earned_report_chart": earned_data,
        "bought_report_chart": bought_data,
        "sold_report_chart": sold_data,
    }

class EarnedBoughtSoldChart(APIView):

    def get(self, request, format=None):
        filter_data = request.GET.dict()

        yesterday = (date.today() - timedelta(days=1))
        data_to_send = None
        if request.GET.get('date') == yesterday.strftime("%Y-%m-%d"):
            data_to_send = cache.get(yesterday.strftime("%Y-%m-%d"))

        if data_to_send is None:
            if ('date' not in request.GET) & ('date__gt' in request.GET) & ('date__lt' in request.GET) & (
                    request.GET.get('date__gt') != request.GET.get('date__lt')):
                # get_serialized_queried data
                filter_data['date__gt'] = datetime.strptime(request.GET.get('date__gt'), CHART_DATE_FORMAT_FOR_DATETIME)
                filter_data['date__lt'] = datetime.strptime(request.GET.get('date__lt'), CHART_DATE_FORMAT_FOR_DATETIME)

                logging.warning(filter_data)
                day_range = filter_data['date__lt'] - filter_data['date__gt']
                day_range = day_range.days + 1
                initial_date = filter_data['date__gt']
                last_date = filter_data['date__lt']
                last_value_from_cache = True
                temp_filter = filter_data.copy()
                bought_data = []
                sold_data = []
                earned_data = []

                for counting_days in range(0, day_range):
                    day = initial_date + timedelta(days=counting_days)
                    cache_key = generate_cache_key(filter_data, day)
                    cache_value = cache.get(cache_key)

                    if cache_value is not None:
                        if not last_value_from_cache:
                            temp_filter['date__lt'] = day
                            not_cached_chart_data = get_chart_data(filter_data=temp_filter)
                            bought_data.extend(not_cached_chart_data.get("bought_report_chart"))
                            sold_data.extend(not_cached_chart_data.get("sold_report_chart"))
                            earned_data.extend(not_cached_chart_data.get("earned_report_chart"))

                        bought_data.append(cache_value['earned_report_chart'])
                        sold_data.append(cache_value['bought_report_chart'])
                        earned_data.append(cache_value['sold_report_chart'])
                        last_value_from_cache = True

                    else:
                        if day == last_date:
                            logging.warning('List ended')
                            temp_filter['date__lt'] = day
                            not_cached_chart_data = get_chart_data(filter_data=temp_filter)
                            bought_data.extend(not_cached_chart_data.get("bought_report_chart"))
                            sold_data.extend(not_cached_chart_data.get("sold_report_chart"))
                            earned_data.extend(not_cached_chart_data.get("earned_report_chart"))
                        else:
                            if last_value_from_cache:
                                temp_filter['date__gt'] = day
                        last_value_from_cache = False

                chart_date_format_message = CHART_DATE_FORMAT_FOR_AMCHARTS

            else:
                date_required = filter_data.get('date')
                data_to_send = cache.get(date_required)
                if data_to_send is None:
                    # get_serialized_queried_data_hourly
                    filter_data['date__gt'] = datetime.strptime(filter_data.get('date'), CHART_DATE_FORMAT_FOR_DATETIME)
                    filter_data['date__gt'] = filter_data['date__gt'] - timedelta(seconds=1)
                    filter_data['date__lt'] = filter_data['date__gt'] + timedelta(days=1)
                    filter_data.pop('date')
                    logging.warning(filter_data)

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
                    earned_data = earned_serializer.data.get("earned_report_chart")
                    chart_date_format_message = CHART_DATETIME_FORMAT_FOR_AMCHARTS

            data_to_send = {
                "earned_report_chart": earned_data,
                "bought_report_chart": bought_data,
                "sold_report_chart": sold_data,
                "chart_date_format": chart_date_format_message,
            }

        return JsonResponse(data_to_send)


class BoughtSoldChart(APIView):

    def get(self, request, format=None):
        filter_data = request.GET.dict()

        if request.GET.get('date') is None:
            filter_data['date__gt'] = datetime.strptime(request.GET.get('date__gt'), CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__lt'] = datetime.strptime(request.GET.get('date__lt'), CHART_DATE_FORMAT_FOR_DATETIME)
            logging.warning(filter_data)
            bought_serializer = BuySerializer(data=filter_data)
            bought_serializer.is_valid()
            sold_serializer = SellSerializer(data=filter_data)
            sold_serializer.is_valid()

            chart_date_format_message = CHART_DATE_FORMAT_FOR_AMCHARTS

        else:
            filter_data['date__gt'] = datetime.strptime(filter_data.get('date'), CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__gt'] = filter_data['date__gt'] - timedelta(seconds=1)
            filter_data['date__lt'] = filter_data['date__gt'] + timedelta(days=1)
            filter_data.pop('date')
            logging.warning(filter_data)

            bought_serializer = BuySerializerWithTime(data=filter_data)
            bought_serializer.is_valid()
            sold_serializer = SellSerializerWithTime(data=filter_data)
            sold_serializer.is_valid()

            chart_date_format_message = CHART_DATETIME_FORMAT_FOR_AMCHARTS

        return JsonResponse({
            "bought_report_chart": list(bought_serializer.data.get("bought_report_chart")),
            "sold_report_chart": list(sold_serializer.data.get("sold_report_chart")),
            "chart_date_format": chart_date_format_message,
        })


class BoughtChart(APIView):

    def get(self, request, format=None):
        filter_data = request.GET.dict()

        if request.GET.get('date') is None:
            filter_data['date__gt'] = datetime.strptime(request.GET.get('date__gt'), CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__lt'] = datetime.strptime(request.GET.get('date__lt'), CHART_DATE_FORMAT_FOR_DATETIME)
            logging.warning(filter_data)
            bought_serializer = BuySerializer(data=filter_data)
            bought_serializer.is_valid()

            chart_date_format_message = CHART_DATE_FORMAT_FOR_AMCHARTS

        else:
            filter_data['date__gt'] = datetime.strptime(filter_data.get('date'), CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__gt'] = filter_data['date__gt'] - timedelta(seconds=1)
            filter_data['date__lt'] = filter_data['date__gt'] + timedelta(days=1)
            filter_data.pop('date')
            logging.warning(filter_data)

            bought_serializer = BuySerializerWithTime(data=filter_data)
            bought_serializer.is_valid()

            chart_date_format_message = CHART_DATETIME_FORMAT_FOR_AMCHARTS

        return JsonResponse({
            "bought_report_chart": list(bought_serializer.data.get("bought_report_chart")),
            "chart_date_format": chart_date_format_message,
        })


class SoldChart(APIView):

    def get(self, request, format=None):
        filter_data = request.GET.dict()

        if request.GET.get('date') is None:
            filter_data['date__gt'] = datetime.strptime(request.GET.get('date__gt'), CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__lt'] = datetime.strptime(request.GET.get('date__lt'), CHART_DATE_FORMAT_FOR_DATETIME)
            logging.warning(filter_data)
            sold_serializer = SellSerializer(data=filter_data)
            sold_serializer.is_valid()

            chart_date_format_message = CHART_DATE_FORMAT_FOR_AMCHARTS

        else:
            filter_data['date__gt'] = datetime.strptime(filter_data.get('date'), CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__gt'] = filter_data['date__gt'] - timedelta(seconds=1)
            filter_data['date__lt'] = filter_data['date__gt'] + timedelta(days=1)
            filter_data.pop('date')
            logging.warning(filter_data)

            sold_serializer = SellSerializerWithTime(data=filter_data)
            sold_serializer.is_valid()

            chart_date_format_message = CHART_DATETIME_FORMAT_FOR_AMCHARTS

        return JsonResponse({
            "sold_report_chart": list(sold_serializer.data.get("sold_report_chart")),
            "chart_date_format": chart_date_format_message,
        })
