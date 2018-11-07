from datetime import datetime, timedelta
import logging

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import BuySerializer, SellSerializer, EarnSerializer, BuySerializerWithTime, \
    SellSerializerWithTime, EarnSerializerWithTime

from mega_market_core.models import CHART_DATE_FORMAT_FOR_DATETIME, CHART_DATE_FORMAT_FOR_AMCHARTS, \
    CHART_DATETIME_FORMAT_FOR_AMCHARTS


class EarnedBoughtSoldChart(APIView):

    def get(self, request, format=None):
        filter_data = request.GET.dict()

        if request.GET.get('date') is None:
            filter_data['date__gt'] = datetime.strptime(request.GET['date__gt'], CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__lt'] = datetime.strptime(request.GET['date__lt'], CHART_DATE_FORMAT_FOR_DATETIME)
            logging.warning(filter_data)
            bought_serializer = BuySerializer(data=filter_data)
            bought_serializer.is_valid()
            sold_serializer = SellSerializer(data=filter_data)
            sold_serializer.is_valid()
            earned_serializer = EarnSerializer(data=filter_data)
            earned_serializer.is_valid()

            return JsonResponse({
                "earned_report_chart": earned_serializer.data.get("earned_report_chart"),
                "bought_report_chart": list(bought_serializer.data.get("bought_report_chart")),
                "sold_report_chart": list(sold_serializer.data.get("sold_report_chart")),
                "chart_date_format": CHART_DATE_FORMAT_FOR_AMCHARTS,
            })
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
            earned_serializer = EarnSerializerWithTime(data=filter_data)
            earned_serializer.is_valid()

            return JsonResponse({
                "earned_report_chart": earned_serializer.data.get("earned_report_chart"),
                "bought_report_chart": list(bought_serializer.data.get("bought_report_chart")),
                "sold_report_chart": list(sold_serializer.data.get("sold_report_chart")),
                "chart_date_format": CHART_DATETIME_FORMAT_FOR_AMCHARTS,
            })


class BoughtSoldChart(APIView):

    def get(self, request, format=None):
        filter_data = request.GET.dict()

        if request.GET.get('date') is None:
            filter_data['date__gt'] = datetime.strptime(request.GET['date__gt'], CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__lt'] = datetime.strptime(request.GET['date__lt'], CHART_DATE_FORMAT_FOR_DATETIME)
        else:
            filter_data['date__gt'] = datetime.strptime(request.GET['date'], CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__lt'] = filter_data['date__gt'] + datetime.timedelta(days=1)

        logging.warning(filter_data)
        bought_serializer = BuySerializer(data=filter_data)
        bought_serializer.is_valid()

        sold_serializer = SellSerializer(data=filter_data)
        sold_serializer.is_valid()

        return JsonResponse({
            "bought_report_chart": list(bought_serializer.data.get("bought_report_chart")),
            "sold_report_chart": list(sold_serializer.data.get("sold_report_chart")),
            "chart_date_format": CHART_DATETIME_FORMAT_FOR_AMCHARTS,
        })


class BoughtChart(APIView):

    def get(self, request, format=None):
        filter_data = request.GET.dict()

        if request.GET.get('date') is None:
            filter_data['date__gt'] = datetime.strptime(request.GET['date__gt'], CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__lt'] = datetime.strptime(request.GET['date__lt'], CHART_DATE_FORMAT_FOR_DATETIME)
        else:
            filter_data['date__gt'] = datetime.strptime(request.GET['date'], CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__lt'] = filter_data['date__gt'] + datetime.timedelta(days=1)

        logging.warning(filter_data)

        bought_serializer = BuySerializer(data=filter_data)
        bought_serializer.is_valid()

        return JsonResponse({
            "bought_report_chart": list(bought_serializer.data.get("bought_report_chart")),
            "chart_date_format": CHART_DATETIME_FORMAT_FOR_AMCHARTS,
        })

class SoldChart(APIView):

    def get(self, request, format=None):
        filter_data = request.GET.dict()

        if request.GET.get('date') is None:
            filter_data['date__gt'] = datetime.strptime(request.GET['date__gt'], CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__lt'] = datetime.strptime(request.GET['date__lt'], CHART_DATE_FORMAT_FOR_DATETIME)
        else:
            filter_data['date__gt'] = datetime.strptime(request.GET['date'], CHART_DATE_FORMAT_FOR_DATETIME)
            filter_data['date__lt'] = filter_data['date__gt'] + datetime.timedelta(days=1)

        logging.warning(filter_data)

        sold_serializer = SellSerializer(data=filter_data)
        sold_serializer.is_valid()

        return JsonResponse({
            "sold_report_chart": list(sold_serializer.data.get("sold_report_chart")),
            "chart_date_format": CHART_DATETIME_FORMAT_FOR_AMCHARTS,
        })
