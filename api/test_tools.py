from collections import OrderedDict
from datetime import datetime

from mega_market_core.models import Geo, Category, SubCategory, Item, TargetUser, Buy, Sell


def basic_transaction_generation():
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

    temp_date = datetime(2018, 10, 10, 0, 0, 0)

    temp_transaction = Buy(
        item=temp_item,
        amount=initial_amount,
        unit_price=initial_unit_price,
        target_user=temp_user,
        date=temp_date,
        geo=temp_geo,
    )
    temp_transaction.save()

    temp_date = datetime(2018, 10, 10, 1, 0, 0)

    temp_transaction = Buy(
        item=temp_item,
        amount=initial_amount,
        unit_price=initial_unit_price,
        target_user=temp_user,
        date=temp_date,
        geo=temp_geo,
    )
    temp_transaction.save()

    temp_date = datetime(2018, 10, 11, 0, 0, 0)

    temp_transaction = Buy(
        item=temp_item,
        amount=initial_amount,
        unit_price=initial_unit_price,
        target_user=temp_user,
        date=temp_date,
        geo=temp_geo,
    )
    temp_transaction.save()

    temp_date = datetime(2018, 10, 11, 1, 0, 0)

    temp_transaction = Buy(
        item=temp_item,
        amount=initial_amount,
        unit_price=initial_unit_price,
        target_user=temp_user,
        date=temp_date,
        geo=temp_geo,
    )
    temp_transaction.save()

    temp_date = datetime(2018, 10, 10, 0, 0, 0)

    temp_transaction = Sell(
        item=temp_item,
        amount=initial_amount,
        unit_price=initial_unit_price,
        target_user=temp_user,
        date=temp_date,
        geo=temp_geo,
    )
    temp_transaction.save()

    temp_date = datetime(2018, 10, 10, 1, 0, 0)

    temp_transaction = Sell(
        item=temp_item,
        amount=initial_amount,
        unit_price=initial_unit_price,
        target_user=temp_user,
        date=temp_date,
        geo=temp_geo,
    )
    temp_transaction.save()

    temp_date = datetime(2018, 10, 11, 0, 0, 0)

    temp_transaction = Sell(
        item=temp_item,
        amount=initial_amount,
        unit_price=initial_unit_price,
        target_user=temp_user,
        date=temp_date,
        geo=temp_geo,
    )
    temp_transaction.save()

    temp_date = datetime(2018, 10, 11, 1, 0, 0)

    temp_transaction = Sell(
        item=temp_item,
        amount=initial_amount,
        unit_price=initial_unit_price,
        target_user=temp_user,
        date=temp_date,
        geo=temp_geo,
    )
    temp_transaction.save()


def full_category_expected_response():
    expected_response = OrderedDict()
    expected_response['name'] = 'Category1'
    expected_response['id'] = 1
    expected_response['subcategories'] = []
    expected_response['subcategories'].append(OrderedDict())
    expected_response['subcategories'][0]['name'] = 'SubCategory1'
    expected_response['subcategories'][0]['id'] = 1
    expected_response['subcategories'][0]['items'] = []
    expected_response['subcategories'][0]['items'].append(OrderedDict())
    expected_response['subcategories'][0]['items'][0]['name'] = 'Item1'
    expected_response['subcategories'][0]['items'][0]['id'] = 1
    return expected_response

