import logging
from datetime import date, timedelta, datetime
from random import randrange

from mega_market_core.models import Category, SubCategory, Item, Geo, TargetUser, Buy, Sell

INITIAL_AMOUNT = 1000
MAX_INITIAL_UNIT_PRICE = 100
MAX_INITIAL_UNIT_PRICE_STEP = 1
INITIAL_DATE = datetime(2018, 7, 1, 0, 0, 0)
TRANSACTION_AMOUNT = 100
DAY_RANGE = 10
MAX_DAILY_TRANSACTION = 100


def data_generator(initial_amount=INITIAL_AMOUNT,
                   max_initial_unit_price=MAX_INITIAL_UNIT_PRICE,
                   max_initial_unit_price_step=MAX_INITIAL_UNIT_PRICE_STEP,
                   initial_date=INITIAL_DATE,
                   day_range=DAY_RANGE,
                   max_daily_transaction=MAX_DAILY_TRANSACTION):
    unit_prices = []
    temp_geo = Geo(country='Uruguay', city='Montevideo', id=1)
    temp_geo.save()
    temp_geo = Geo(country='Argentina', city='Buenos Aires', id=2)
    temp_geo.save()
    temp_geo = Geo(country='Brasil', city='Rio de Janeiro', id=3)
    temp_geo.save()

    for i in range(1, 6):
        temp_category = Category(name='Category%s' % i, id=i)
        temp_category.save()
        temp_sub_category = SubCategory(name='SubCategory%s' % i, category_id=i, id=i)
        temp_sub_category.save()
        temp_item = Item(name='Item%s' % i, sub_category_id=i, id=i)
        temp_item.save()
        temp_user = TargetUser(name='target_user_%s' % i, id=i)
        temp_user.save()
        initial_unit_price = randrange(0, max_initial_unit_price)

        initial_transaction = Buy(
            item=temp_item,
            amount=initial_amount,
            unit_price=initial_unit_price,
            date=initial_date,
            target_user_id=i,
            geo=temp_geo,
            currency_code='URU',
            currency_symbol='$U',
            id=i,
        )
        initial_transaction.save()

        unit_prices.append({'Item_id': i, 'unit_price': initial_unit_price, 'stock': initial_amount})

    target_user_amount = TargetUser.objects.all().count()
    item_amount = Item.objects.all().count()
    sub_category_amount = SubCategory.objects.all().count()
    category_amount = Category.objects.all().count()
    geo_amount = Geo.objects.all().count()

    for counting_days in range(0, day_range):
        for i in range(0, max_daily_transaction):
            hours = randrange(0, 24)
            minutes = randrange(0, 60)
            day = initial_date + timedelta(days=counting_days, hours=hours, minutes=minutes)

            target_user_amount_id = randrange(0, target_user_amount) + 1
            temp_item_id = randrange(0, item_amount) + 1
            temp_geo_id = randrange(0, geo_amount) + 1

            if temp_geo_id == 1:
                temp_currency_code = 'UYU',
                temp_currency_symbol = '$U',
            elif temp_geo_id == 2:
                temp_currency_code = 'ARS',
                temp_currency_symbol = '$A',
            elif temp_geo_id == 3:
                temp_currency_code = 'BRL',
                temp_currency_symbol = 'R$',

            transaction_amount = randrange(initial_amount * 0.1, initial_amount * 0.9)
            transaction_price = Item(id=temp_item_id).generate_next_price()

            if randrange(0, 2):
                temp_transaction = Buy(
                    item_id=temp_item_id,
                    amount=transaction_amount,
                    unit_price=transaction_price,
                    date=day,
                    target_user_id=target_user_amount_id,
                    geo_id=temp_geo_id,
                    currency_code=temp_currency_code,
                    currency_symbol=temp_currency_symbol,
                )
            else:
                temp_transaction = Sell(
                    item_id=temp_item_id,
                    amount=transaction_amount,
                    unit_price=transaction_price,
                    date=day,
                    target_user_id=target_user_amount_id,
                    geo_id=temp_geo_id,
                    currency_code=temp_currency_code,
                    currency_symbol=temp_currency_symbol,
                )

            # logging.warning(temp_transaction)
            try:
                temp_transaction.save()
            except Exception as e:
                logging.error(e)
                logging.error('item_id %s' % temp_transaction.item)
                logging.error('item %s' % temp_transaction.item)
                logging.error('amount %s' % temp_transaction.amount)
                logging.error('unit_price %s' % temp_transaction.unit_price)
                logging.error('date %s' % temp_transaction.date)
                logging.error('target_user %s' % temp_transaction.target_user)
                logging.error('geo_id %s' % temp_transaction.geo_id)
                logging.error('currency_code %s' % temp_transaction.currency_code)
                logging.error('currency_symbol %s' % temp_transaction.currency_symbol)
        logging.warning('%s', day)

    return unit_prices
