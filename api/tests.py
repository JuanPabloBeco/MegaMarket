import json

from django.test import TestCase, Client

from datetime import datetime
# Create your tests here.
from django.urls import reverse
import logging

from api.serializers import CategorySerializer, SubCategorySerializer, EarnSerializer, ItemSerializer, BuySerializer, \
    SellSerializer, EarnSerializerWithTime, SellSerializerWithTime, BuySerializerWithTime
from api.test_tools import basic_transaction_generation, full_category_expected_response
from mega_market_core.models import Buy, Category, SubCategory, Item, TargetUser, Geo, Sell


class EarnedBoughtSellAPIEndpointsTest(TestCase):
    def setUp(self):
        client = Client()
        basic_transaction_generation()
        logging.getLogger().setLevel(logging.INFO)

    def test_buy_api_endpoint(self):
        filter_data = {
            "date__lt": "2018-10-12",
            "date__gt": "2018-10-9",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        data_json = json.dumps(filter_data)

        response = self.client.get(reverse('bought'), data=filter_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "bought_report_chart": [
                {"data_sum": 200, "date": "2018-10-10"},
                {"data_sum": 200, "date": "2018-10-11"},
            ],
            "chart_date_format": "YYYY-MM-DD",
        }
        self.assertEqual(json.loads(response.content), expected_response)

    def test_sell_api_endpoint(self):
        filter_data = {
            "date__lt": "2018-10-12",
            "date__gt": "2018-10-9",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        data_json = json.dumps(filter_data)

        response = self.client.get(reverse('sold'), data=filter_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "sold_report_chart": [
                {"date": "2018-10-10", "data_sum": 200},
                {"date": "2018-10-11", "data_sum": 200},
            ],
            "chart_date_format": "YYYY-MM-DD",
        }
        self.assertEqual(json.loads(response.content), expected_response)

    def test_bought_sell_api_endpoint(self):
        filter_data = {
            "date__lt": "2018-10-12",
            "date__gt": "2018-10-9",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        data_json = json.dumps(filter_data)

        response = self.client.get(reverse('boughtsold'), data=filter_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "bought_report_chart": [
                {"date": "2018-10-10", "data_sum": 200},
                {"date": "2018-10-11", "data_sum": 200},
            ],
            "sold_report_chart": [
                {"date": "2018-10-10", "data_sum": 200},
                {"date": "2018-10-11", "data_sum": 200},
            ],
            "chart_date_format": "YYYY-MM-DD",
        }
        self.assertEqual(json.loads(response.content), expected_response)

    def test_earned_bought_sell_api_endpoint(self):
        filter_data = {
            "date__lt": "2018-10-12",
            "date__gt": "2018-10-9",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        data_json = json.dumps(filter_data)

        response = self.client.get(reverse('earnedboughtsold'), data=filter_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "earned_report_chart": [
                {"data_sum": 0, "date": "2018-10-10"},
                {"data_sum": 0, "date": "2018-10-11"},
            ],
            "bought_report_chart": [
                {"data_sum": 200, "date": "2018-10-10"},
                {"data_sum": 200, "date": "2018-10-11"},
            ],
            "sold_report_chart": [
                {"data_sum": 200, "date": "2018-10-10"},
                {"data_sum": 200, "date": "2018-10-11"},
            ],
            "chart_date_format": "YYYY-MM-DD",
        }
        self.assertEqual(json.loads(response.content), expected_response)

    def test_buy_api_endpoint_one_day(self):
        filter_data = {
            "date": "2018-10-11",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        data_json = json.dumps(filter_data)

        response = self.client.get(reverse('bought'), data=filter_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "bought_report_chart": [
                {"data_sum": 100, "date": "2018-10-11 00:00:00"},
                {"data_sum": 100, "date": "2018-10-11 01:00:00"},
            ],
            "chart_date_format": "YYYY-MM-DD JJ:mm:ss",
        }
        self.assertEqual(json.loads(response.content), expected_response)

    def test_sell_api_endpoint_one_day(self):
        filter_data = {
            "date": "2018-10-11",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        data_json = json.dumps(filter_data)

        response = self.client.get(reverse('sold'), data=filter_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "sold_report_chart": [
                {"data_sum": 100, "date": "2018-10-11 00:00:00"},
                {"data_sum": 100, "date": "2018-10-11 01:00:00"},
            ],
            "chart_date_format": "YYYY-MM-DD JJ:mm:ss",
        }
        self.assertEqual(json.loads(response.content), expected_response)

    def test_bought_sell_api_endpoint_one_day(self):
        filter_data = {
            "date": "2018-10-11",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        data_json = json.dumps(filter_data)

        response = self.client.get(reverse('boughtsold'), data=filter_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "bought_report_chart": [
                {"data_sum": 100, "date": "2018-10-11 00:00:00"},
                {"data_sum": 100, "date": "2018-10-11 01:00:00"},
            ],
            "sold_report_chart": [
                {"data_sum": 100, "date": "2018-10-11 00:00:00"},
                {"data_sum": 100, "date": "2018-10-11 01:00:00"},
            ],
            "chart_date_format": "YYYY-MM-DD JJ:mm:ss",
        }
        self.assertEqual(json.loads(response.content), expected_response)

    def test_earned_bought_sell_api_endpoint_one_day(self):
        filter_data = {
            "date": "2018-10-11",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        data_json = json.dumps(filter_data)

        response = self.client.get(reverse('earnedboughtsold'), data=filter_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        expected_response = {
            "earned_report_chart": [
                {"data_sum": 0, "date": "2018-10-11 00:00:00"},
                {"data_sum": 0, "date": "2018-10-11 01:00:00"},
            ],
            "bought_report_chart": [
                {"data_sum": 100, "date": "2018-10-11 00:00:00"},
                {"data_sum": 100, "date": "2018-10-11 01:00:00"},
            ],
            "sold_report_chart": [
                {"data_sum": 100, "date": "2018-10-11 00:00:00"},
                {"data_sum": 100, "date": "2018-10-11 01:00:00"},
            ],
            "chart_date_format": "YYYY-MM-DD JJ:mm:ss",
        }
        self.assertEqual(json.loads(response.content), expected_response)


class CategorySubcategoryItemSerializerTest(TestCase):
    def setUp(self):
        client = Client()
        basic_transaction_generation()
        logging.getLogger().setLevel(logging.INFO)

    def test_category_serializer(self):
        categories = Category.objects.all()
        serializer = CategorySerializer(data=categories, many=True)
        serializer.is_valid()
        logging.info('Serializer data: %s' % serializer.data)

        expected_response = [full_category_expected_response(), ]
        logging.info('Expected response: %s' % expected_response)

        self.assertEqual(serializer.data, expected_response)

    def test_subcategory_serializer(self):
        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(data=list(subcategories), many=True)
        serializer.is_valid()
        logging.info('Serializer data: %s' % serializer.data)

        expected_response = full_category_expected_response().get('subcategories')
        logging.info('Expected response: %s' % expected_response)

        self.assertEqual(serializer.data, expected_response)

    def test_item_serializer(self):
        items = Item.objects.all()
        serializer = ItemSerializer(data=list(items), many=True)
        serializer.is_valid()
        logging.info('Serializer data: %s' % serializer.data)

        expected_response = full_category_expected_response().get('subcategories')
        expected_response = expected_response[0].get('items')
        logging.info('Expected response: %s' % expected_response)

        self.assertEqual(serializer.data, expected_response)


class EarnedBoughtSellSerializerTest(TestCase):
    def setUp(self):
        client = Client()
        basic_transaction_generation()
        logging.getLogger().setLevel(logging.INFO)

    def test_buy_serializer_ok(self):
        filter_data = {
            "date__lt": "2018-10-12",
            "date__gt": "2018-10-9",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        serializer = BuySerializer(data=filter_data)
        serializer.is_valid()
        logging.info('Serializer data: %s' % serializer.data)

        bought_list = Buy.get_bought_list_by_date_filtered(**filter_data)
        logging.info(bought_list)

        expected_response = [
            {"date": "2018-10-10", "data_sum": 200},
            {"date": "2018-10-11", "data_sum": 200},
        ]
        self.assertEqual(list(serializer.data.get('bought_report_chart')), expected_response)

    def test_sold_serializer_ok(self):
        filter_data = {
            "date__lt": "2018-10-12",
            "date__gt": "2018-10-9",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        serializer = SellSerializer(data=filter_data)
        serializer.is_valid()
        logging.info('Serializer data: %s' % serializer.data)

        sold_list = Sell.get_sold_list_by_date_filtered(**filter_data)
        logging.info(sold_list)

        expected_response = [
            {"date": "2018-10-10", "data_sum": 200},
            {"date": "2018-10-11", "data_sum": 200},
        ]
        self.assertEqual(list(serializer.data.get('sold_report_chart')), expected_response)

    def test_earn_serializer_ok(self):
        end_date = datetime(2018, 10, 12)
        start_date = datetime(2018, 10, 9)
        filter_data = {
            "date__lt": end_date,
            "date__gt": start_date,
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        serializer = EarnSerializer(data=filter_data)
        serializer.is_valid()
        logging.info('Serializer data: %s' % serializer.data)

        expected_response = [
            {"date": "2018-10-10", "data_sum": 0.0},
            {"date": "2018-10-11", "data_sum": 0.0},
        ]
        self.assertEqual(list(serializer.data.get('earned_report_chart')), expected_response)


class EarnedBoughtSellSerializerTestWithTime(TestCase):
    def setUp(self):
        client = Client()
        basic_transaction_generation()
        logging.getLogger().setLevel(logging.INFO)

    def test_buy_serializer_with_time(self):
        filter_data = {
            "date__lt": "2018-10-12 00:00:00",
            "date__gt": "2018-10-10 11:59:59",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        serializer = BuySerializerWithTime(data=filter_data)
        serializer.is_valid()
        logging.info('Serializer data: %s' % serializer.data)

        bought_list = Buy.get_bought_list_by_date_filtered(**filter_data)
        logging.info(bought_list)

        expected_response = [
            {"data_sum": 100.0, "date": "2018-10-11 00:00:00"},
            {"data_sum": 100.0, "date": "2018-10-11 01:00:00"},
        ]
        self.assertEqual(list(serializer.data.get('bought_report_chart')), expected_response)

    def test_sold_serializer_with_time(self):
        filter_data = {
            "date__lt": "2018-10-12 00:00:00",
            "date__gt": "2018-10-10 11:59:59",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        serializer = SellSerializerWithTime(data=filter_data)
        serializer.is_valid()
        logging.info('Serializer data: %s' % serializer.data)

        expected_response = [
            {"data_sum": 100.0, "date": "2018-10-11 00:00:00"},
            {"data_sum": 100.0, "date": "2018-10-11 01:00:00"},
        ]
        self.assertEqual(list(serializer.data.get('sold_report_chart')), expected_response)

    def test_earn_serializer_with_time(self):
        end_date = datetime(2018, 10, 12, 0, 0, 0)
        start_date = datetime(2018, 10, 10, 11, 59, 59)
        filter_data = {
            "date__lt": end_date,
            "date__gt": start_date,
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        serializer = EarnSerializerWithTime(data=filter_data)
        serializer.is_valid()
        logging.info('Serializer data: %s' % serializer.data)

        expected_response = [
            {"data_sum": 0.0, "date": "2018-10-11 00:00:00"},
            {"data_sum": 0.0, "date": "2018-10-11 01:00:00"},
        ]
        self.assertEqual(list(serializer.data.get('earned_report_chart')), expected_response)


class BoughtSellQueryTest(TestCase):
    def setUp(self):
        basic_transaction_generation()

    def test_bought_get_list_days(self):
        filter_data = {
            "date__lt": "2018-10-12",
            "date__gt": "2018-10-9",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        bought_list = Buy.get_bought_list_by_date_filtered(**filter_data)
        logging.warning(bought_list)

        expected_response = [
            {"date": "2018-10-10", "data_sum": 200},
            {"date": "2018-10-11", "data_sum": 200},
        ]
        self.assertEqual(list(bought_list), expected_response)

    def test_bought_get_list_hours(self):
        filter_data = {
            "date__lt": "2018-10-12 00:00:00",
            "date__gt": "2018-10-10 11:59:59",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        bought_list = Buy.get_bought_one_day_list_by_date_filtered(**filter_data)
        logging.warning(bought_list)

        expected_response = [
            {"date": "2018-10-11 00:00:00", "data_sum": 100},
            {"date": "2018-10-11 01:00:00", "data_sum": 100},
        ]
        self.assertEqual(list(bought_list), expected_response)

    def test_sold_get_list_days(self):
        filter_data = {
            "date__lt": "2018-10-12",
            "date__gt": "2018-10-9",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        sold_list = Sell.get_sold_list_by_date_filtered(**filter_data)
        logging.warning(sold_list)
        expected_response = [
            {"date": "2018-10-10", "data_sum": 200},
            {"date": "2018-10-11", "data_sum": 200},
        ]
        self.assertEqual(list(sold_list), expected_response)

    def test_sold_get_list_hours(self):
        filter_data = {
            "date__lt": "2018-10-12 00:00:00",
            "date__gt": "2018-10-10 11:59:59",
            "item_id": 1,
            "geo_id": 1,
            "target_user_id": 1,
        }
        sold_list = Sell.get_sold_one_day_list_by_date_filtered(**filter_data)
        logging.warning(sold_list)
        expected_response = [
            {"date": "2018-10-11 00:00:00", "data_sum": 100},
            {"date": "2018-10-11 01:00:00", "data_sum": 100},
        ]
        self.assertEqual(list(sold_list), expected_response)
