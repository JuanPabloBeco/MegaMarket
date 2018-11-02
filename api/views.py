from datetime import datetime
import logging

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import BuySerializer, SellSerializer, EarnSerializer

from mega_market_core.models import Buy, CHART_DATE_FORMAT_FOR_DATETIME


class EarnedBoughtSoldChart(APIView):

    def get(self, request, format=None):
        filter_data = request.GET.dict()

        # filter_data.pop('csrfmiddlewaretoken')
        filter_data['date__lt'] = datetime.strptime(request.GET['date__lt'], CHART_DATE_FORMAT_FOR_DATETIME)
        filter_data['date__gt'] = datetime.strptime(request.GET['date__gt'], CHART_DATE_FORMAT_FOR_DATETIME)

        logging.warning(filter_data)
        bought_serializer = BuySerializer(data=filter_data)
        bought_serializer.is_valid()

        sold_serializer = SellSerializer(data=filter_data)
        sold_serializer.is_valid()

        earned_serializer = EarnSerializer(data=filter_data)
        earned_serializer.is_valid()

        return Response({
            "earned_report_chart": earned_serializer.data.get("earned_report_chart"),
            "bought_report_chart": bought_serializer.data.get("bought_report_chart"),
            "sold_report_chart": sold_serializer.data.get("sold_report_chart"),
        }, status=status.HTTP_200_OK)


class BoughtSoldChart(APIView):

    def get(self, request, format=None):
        filter_data = request.GET.dict()

        # filter_data.pop('csrfmiddlewaretoken')
        filter_data['date__lt'] = datetime.strptime(request.GET['date__lt'], CHART_DATE_FORMAT_FOR_DATETIME)
        filter_data['date__gt'] = datetime.strptime(request.GET['date__gt'], CHART_DATE_FORMAT_FOR_DATETIME)

        logging.warning(filter_data)
        bought_serializer = BuySerializer(data=filter_data)
        bought_serializer.is_valid()

        sold_serializer = SellSerializer(data=filter_data)
        sold_serializer.is_valid()

        return Response({
            "bought_report_chart": bought_serializer.data.get("bought_report_chart"),
            "sold_report_chart": sold_serializer.data.get("sold_report_chart"),
        }, status=status.HTTP_200_OK)


class BoughtChart(APIView):

    def get(self, request, format=None):
        filter_data = request.GET.dict()

        # filter_data.pop('csrfmiddlewaretoken')
        filter_data['date__lt'] = datetime.strptime(request.GET['date__lt'], CHART_DATE_FORMAT_FOR_DATETIME)
        filter_data['date__gt'] = datetime.strptime(request.GET['date__gt'], CHART_DATE_FORMAT_FOR_DATETIME)

        logging.warning(filter_data)
        serializer = BuySerializer(data=filter_data)

        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class SoldChart(APIView):

    def get(self, request, format=None):
        filter_data = request.GET.dict()

        # filter_data.pop('csrfmiddlewaretoken')
        filter_data['date__lt'] = datetime.strptime(request.GET['date__lt'], CHART_DATE_FORMAT_FOR_DATETIME)
        filter_data['date__gt'] = datetime.strptime(request.GET['date__gt'], CHART_DATE_FORMAT_FOR_DATETIME)

        logging.warning(filter_data)
        serializer = SellSerializer(data=filter_data)

        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)
