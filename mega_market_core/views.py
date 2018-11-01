from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.utils import json

from api.serializers import CategorySerializer, GeoSerializer, TargetUserSerializer
from api.views import BoughtChart
from mega_market_core.forms import TransactionForm
from mega_market_core.models import CHART_DATE_FORMAT_FOR_AMCHARTS, Category, Geo, TargetUser

GET = 'GET'
POST = 'POST'


def dashboard(request):
    """
    View used for the dashboard page with the ticket to add more transactions
    :param request:
    :return:
    """

    if request.method == GET:
        form = TransactionForm()

        categories = Category.objects.all()
        category_subcategory_item_filter_serializer = CategorySerializer(data=categories, many=True)
        category_subcategory_item_filter_serializer.is_valid()
        category_subcategory_item_filter_serializer_json = json.dumps(category_subcategory_item_filter_serializer.data)

        geos = Geo.objects.all()
        geo_filter_serializer = GeoSerializer(data=geos, many=True)
        geo_filter_serializer.is_valid()
        geo_filter_serializer_json = json.dumps(geo_filter_serializer.data)

        target_users = TargetUser.objects.all()
        target_user_filter_serializer = TargetUserSerializer(data=target_users, many=True)
        target_user_filter_serializer.is_valid()
        target_user_filter_serializer_json = json.dumps(target_user_filter_serializer.data)

        return render(request, 'dashboard.html', {
            'form': form,
            'chart_date_format': CHART_DATE_FORMAT_FOR_AMCHARTS,
            'categories_subcategories_items_filter_options': category_subcategory_item_filter_serializer_json,
            'geo_filter_options': geo_filter_serializer_json,
            'target_user_filter_options': target_user_filter_serializer_json,
        })

    elif request.method == POST:
        form = TransactionForm(request.POST)
        template = 'dashboard.html'

    else:
        response = redirect(reverse('dashboard'))
        return response
