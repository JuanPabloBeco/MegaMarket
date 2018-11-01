from rest_framework import serializers

from mega_market_core.models import Buy, Category, SubCategory, Item, Geo, TargetUser, Sell


class BuySerializer(serializers.Serializer):
    # The serializer look for this in the entry data and when found goes to the method
    bought_report_chart = serializers.SerializerMethodField()

    def get_bought_report_chart(self, obj):
        filters = self.initial_data
        bought_list = Buy.get_bought_list_by_date_filtered(**filters)

        return bought_list


class SellSerializer(serializers.Serializer):
    # The serializer look for this in the entry data and when found goes to the method
    sold_report_chart = serializers.SerializerMethodField()

    def get_sold_report_chart(self, obj):
        filters = self.initial_data
        bought_list = Sell.get_sold_list_by_date_filtered(**filters)

        return bought_list


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
    
from api.serializers import BuySerializer
data = {
            "date_to": "2018-10-31",
            "date_from": "2018-9-1",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
a=BuySerializer(data=data)
a.is_valid()
a.data
    
    """