from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from datetime import datetime, timedelta

from MegaMarket.celery import DAILY_OPENING_API_REQUEST_CACHE_INTERVAL_SECONDS
from api.cache_tools import set_one_day_data_to_cache
from mega_market_core.models import Buy, Category, SubCategory, Item, Geo, TargetUser, Sell, \
    CHART_DATE_FORMAT_FOR_DATETIME


class BuySerializer(serializers.Serializer):
    # The serializer look for this in the entry data and when found goes to the method
    bought_report_chart = serializers.SerializerMethodField()

    def get_bought_report_chart(self, obj):
        filters = self.initial_data
        if filters.get('date') is not None:
            filters.pop('date')
            bought_list = Buy.get_bought_one_day_list_by_date_filtered(**filters)
        else:
            bought_list = Buy.get_bought_list_by_date_filtered(**filters)
        for i in bought_list:
            i["data_sum"] = round(i.get("data_sum"), 2)

        return bought_list


class SellSerializer(serializers.Serializer):
    sold_report_chart = serializers.SerializerMethodField()

    def get_sold_report_chart(self, obj):
        filters = self.initial_data
        if filters.get('date') is not None:
            sold_list = Sell.get_sold_one_day_list_by_date_filtered(**filters)
        else:
            sold_list = Sell.get_sold_list_by_date_filtered(**filters)

        for i in sold_list:
            i["data_sum"] = round(i.get("data_sum"), 2)

        return sold_list


class EarnSerializer(serializers.Serializer):
    earned_report_chart = serializers.SerializerMethodField()

    def get_earned_report_chart(self, obj):
        send_to_cache = self.initial_data['send_to_cache']

        bought_list = self.initial_data.get('bought_data')
        sold_list = self.initial_data.get('sold_data')

        until_date = self.initial_data.get("filter_data").get("date__lt")
        from_date = self.initial_data.get("filter_data").get("date__gt")

        earned_list = []

        dayrange = (until_date - from_date).days

        date_sold_dict = {}
        for obj in sold_list:
            date_sold_dict[obj.get('date')] = obj
        date_bought_dict = {}
        for obj in bought_list:
            date_bought_dict[obj.get('date')] = obj

        # Daily earned
        for i in range(0, dayrange):
            day = from_date + timedelta(days=i)
            day = day.strftime(CHART_DATE_FORMAT_FOR_DATETIME)
            sold_this_date = date_sold_dict.get(day)
            bought_this_date = date_bought_dict.get(day)

            if (sold_this_date is not None) & (bought_this_date is not None):
                # This must stay only until values are assign to the emtpy earned dates
                if sold_this_date and bought_this_date:
                    earned_this_date = {
                        'data_sum': round(sold_this_date.get('data_sum') - bought_this_date.get('data_sum'), 2),
                        'date': day}
                elif sold_this_date:
                    earned_this_date = {'data_sum': sold_this_date.get('data_sum'), 'date': day}
                elif bought_this_date:
                    earned_this_date = {'data_sum': - bought_this_date.get('data_sum'), 'date': day}

                earned_list.append(earned_this_date)
                if send_to_cache:
                    set_one_day_data_to_cache(
                        earned_this_date,
                        bought_this_date,
                        sold_this_date,
                        self.initial_data.get("filter_data"),
                        day,
                        DAILY_OPENING_API_REQUEST_CACHE_INTERVAL_SECONDS,
                    )
            else:
                earned_this_date = {'data_sum': 0, 'date': day}

        return earned_list


class BuySerializerWithTime(serializers.Serializer):
    # The serializer look for this in the entry data and when found goes to the method
    bought_report_chart = serializers.SerializerMethodField()

    def get_bought_report_chart(self, obj):
        filters = self.initial_data
        bought_list = Buy.get_bought_one_day_list_by_date_filtered(**filters)

        for i in bought_list:
            i["data_sum"] = round(i.get("data_sum"), 2)

        return bought_list


class SellSerializerWithTime(serializers.Serializer):
    sold_report_chart = serializers.SerializerMethodField()

    def get_sold_report_chart(self, obj):
        filters = self.initial_data
        sold_list = Sell.get_sold_one_day_list_by_date_filtered(**filters)

        for i in sold_list:
            i["data_sum"] = round(i.get("data_sum"), 2)

        return sold_list


class EarnSerializerWithTime(serializers.Serializer):
    earned_report_chart = serializers.SerializerMethodField()

    def get_earned_report_chart(self, obj):
        send_to_cache = self.initial_data['send_to_cache']

        bought_list = self.initial_data.get('bought_data')
        sold_list = self.initial_data.get('sold_data')

        bought_iterator = 0
        bought_ended = False
        sold_iterator = 0
        sold_ended = False
        earned_list = []

        for i in range(0, bought_list.__len__() + sold_list.__len__()):
            try:
                # Its supposed that the Querysets are ordered by date
                bought_this_date = bought_list[bought_iterator]
            except IndexError:
                # 9999 is used because the following code registers the smaller date first
                bought_this_date = {'data_sum': 0, 'date': '9999-01-01 00:00:00'}
                bought_ended = True

            try:
                # Its supposed that the Querysets are ordered by date
                sold_this_date = sold_list[sold_iterator]
            except IndexError:
                # 9999 is used because the following code registers the smaller date first
                sold_this_date = {'data_sum': 0, 'date': '9999-01-01 00:00:00'}
                sold_ended = True

            if bought_ended & sold_ended:
                break

            if (bought_this_date.get('date') < sold_this_date.get('date')) | sold_ended:
                earned_this_date = {'data_sum': - bought_this_date.get('data_sum'),
                                    'date': bought_this_date.get('date')}

                bought_iterator += 1

            elif (bought_this_date.get('date') > sold_this_date.get('date')) | bought_ended:
                earned_this_date = {'data_sum': sold_this_date.get('data_sum'), 'date': sold_this_date.get('date')}
                sold_iterator += 1

            else:
                # Day to day earning
                earned_this_date = {
                    'data_sum': round(sold_this_date.get('data_sum') - bought_this_date.get('data_sum'), 2),
                    'date': bought_this_date.get('date')}
                bought_iterator += 1
                sold_iterator += 1
            earned_list.append(earned_this_date)
            if send_to_cache:
                set_one_day_data_to_cache(
                    earned_this_date,
                    bought_this_date,
                    sold_this_date,
                    self.initial_data.get("filter_data"),
                    earned_this_date.get('date')
                )
        return earned_list


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    def get_subcategories(self, obj):
        serializer = SubCategorySerializer(obj.sub_category.all(), many=True)
        data = serializer.data
        return data

    class Meta:
        model = Category
        fields = ('name', 'id', 'subcategories')


class SubCategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        serializer = ItemSerializer(obj.items.all(), many=True)
        data = serializer.data
        return data

    class Meta:
        model = SubCategory
        fields = ('name', 'id', 'items')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'id')


class TargetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetUser
        fields = ('name', 'id')


class GeoSerializer(serializers.ModelSerializer):
    city_and_country = serializers.SerializerMethodField()

    def get_city_and_country(self, obj):
        serializer = "%s, %s" % (obj.city, obj.country)
        return serializer

    class Meta:
        model = Geo
        fields = ('city_and_country', 'id')

    """
Filter format
data = {
            "date__lt": "2018-10-31",
            "date__gt": "2018-9-1",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
    
    """


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