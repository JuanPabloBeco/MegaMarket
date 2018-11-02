import json

from django.test import TestCase, Client

from datetime import datetime
# Create your tests here.
from django.urls import reverse
from django.utils import log
import logging

from api.serializers import CategorySerializer, SubCategorySerializer, EarnSerializer
from mega_market_core.models import Buy, Category, SubCategory, Item, TargetUser, Geo


class BuySerializerTest(TestCase):
    def setUp(self):
        client = Client()

        temp_geo = Geo(country='Uruguay', id=1)
        temp_geo.save()
        temp_category = Category(name='Category%s' % 1, id=1)
        temp_category.save()
        temp_sub_category = SubCategory(name='SubCategory%s' % 1, category_id=1, id=1)
        temp_sub_category.save()
        temp_item = Item(name='Item%s' % 1, sub_category_id=1, id=1)
        temp_item.save()
        temp_user = TargetUser(name='target_user_%s' % 1, id=1)
        temp_user.save()
        initial_unit_price = 10
        initial_amount = 10

        temp_date = datetime(2018, 10, 1, 0, 0, 0)
        initial_transaction = Buy(
            item=temp_item,
            amount=initial_amount,
            unit_price=initial_unit_price,
            date=temp_date,
            target_user=temp_user,
            geo=temp_geo,
        )
        initial_transaction.save()
        initial_transaction = Buy(
            item=temp_item,
            amount=initial_amount,
            unit_price=initial_unit_price,
            date=temp_date,
            target_user=temp_user,
            geo=temp_geo,
        )
        initial_transaction.save()

        temp_date = datetime(2018, 10, 2, 0, 0, 0)
        initial_transaction = Buy(
            item=temp_item,
            amount=initial_amount,
            unit_price=initial_unit_price,
            date=temp_date,
            target_user=temp_user,
            geo=temp_geo,
        )
        initial_transaction.save()

    def test_buy_serializer(self):
        data = {
            "date__lt": "2018-10-2",
            "date__gt": "2018-9-1",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        data_json = json.dumps(data)

        response = self.client.get(reverse('bought'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "bought_report_chart": [
                {"date": "2018-10-01", "data_sum": 10},
                {"date": "2018-10-02", "data_sum": 10},
            ]
        }

        self.assertEqual(response.data, expected_response)

    def test_buy_get_list(self):
        data = {
            "date__lt": "2018-10-2",
            "date__gt": "2018-9-1",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        bought_list = Buy.get_bought_list_by_date_filtered(**data)
        logging.warning(bought_list)
        self.assertEqual(bought_list.count(), 1)

    def test_category_serializer(self):
        categories = Category.objects.all()
        serializer = CategorySerializer(data=categories, many=True)
        serializer.is_valid()
        logging.warning(serializer.data)
        expected_response = {
            'name': 'Category1', 'id': 1,
            'subcategories': [[('name', 'SubCategory1'), ('id', 1)]]
        }
        self.assertEqual(dict(serializer.data[0]), expected_response)

    def test_subcategory_serializer(self):
        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(data=list(subcategories))
        serializer.is_valid()
        logging.warning(serializer.data)
        expected_response = {
            'name': 'Category1',
            'id': 1
        }
        self.assertEqual(dict(serializer.data[0]), expected_response)

