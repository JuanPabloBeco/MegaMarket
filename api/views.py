from datetime import datetime
import logging

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import BuySerializer

from mega_market_core.models import Buy, CHART_DATE_FORMAT_FOR_DATETIME


class BoughtChart(APIView):

    def get(self, request, format=None):

        filter_data = request.GET.dict()

        # filter_data.pop('csrfmiddlewaretoken')
        filter_data['date__lt'] = datetime.strptime(request.GET['date__lt'], CHART_DATE_FORMAT_FOR_DATETIME)
        filter_data['date__gt'] = datetime.strptime(request.GET['date__gt'], CHART_DATE_FORMAT_FOR_DATETIME)

        logging.info('Chart requested with these filters:-----------------------------------')
        logging.info(filter_data)
        logging.info('----------------------------------------------------------------------')
        serializer = BuySerializer(data=filter_data)

        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)
