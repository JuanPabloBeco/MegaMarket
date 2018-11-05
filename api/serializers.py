from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from datetime import datetime, timedelta

from mega_market_core.models import Buy, Category, SubCategory, Item, Geo, TargetUser, Sell, \
    CHART_DATE_FORMAT_FOR_DATETIME


class BuySerializer(serializers.Serializer):
    # The serializer look for this in the entry data and when found goes to the method
    bought_report_chart = serializers.SerializerMethodField()

    def get_bought_report_chart(self, obj):
        filters = self.initial_data
        if filters.get('date') is not None:
            bought_list = Buy.get_bought_one_day_list_filtered(**filters)
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
            sold_list = Sell.get_sold_one_day_list_filtered(**filters)
        else:
            sold_list = Sell.get_sold_list_by_date_filtered(**filters)

        for i in sold_list:
            i["data_sum"] = round(i.get("data_sum"), 2)

        return sold_list


class EarnSerializer(serializers.Serializer):
    earned_report_chart = serializers.SerializerMethodField()

    def get_earned_report_chart(self, obj):
        filters = self.initial_data

        if filters.get('date') is not None:
            bought_list = Buy.get_bought_one_day_list_filtered(**filters)
            sold_list = Sell.get_sold_one_day_list_filtered(**filters)
        else:
            bought_list = Buy.get_bought_list_by_date_filtered(**filters)
            sold_list = Sell.get_sold_list_by_date_filtered(**filters)

        until_date = self.initial_data.get("date__lt")
        from_date = self.initial_data.get("date__gt")

        earned_list = []

        dayrange = (until_date - from_date).days

        date_sold_dict = {}
        for obj in sold_list:
            date_sold_dict[obj.get('date')] = obj
        date_bought_dict = {}
        for obj in bought_list:
            date_bought_dict[obj.get('date')] = obj

        for i in range(0, dayrange):
            day = from_date + timedelta(days=i)
            day = datetime.strftime(day, CHART_DATE_FORMAT_FOR_DATETIME)
            sold_this_date = date_sold_dict.get(day)
            bought_this_date = date_bought_dict.get(day)

            if sold_this_date and bought_this_date:
                earned_list.append(
                    {'data_sum': round(sold_this_date.get('data_sum') - bought_this_date.get('data_sum'), 2), 'date': day})
            elif sold_this_date:
                earned_list.append({'data_sum': sold_this_date.get('data_sum'), 'date': day})
            elif bought_this_date:
                earned_list.append({'data_sum': - bought_this_date.get('data_sum'), 'date': day})
            # else:
            #     earned_list.append(0)

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
            "date_to": "2018-10-31",
            "date_from": "2018-9-1",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
    
    """
