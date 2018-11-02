from datetime import datetime, timedelta
from random import randrange

import logging

from celery import shared_task

from mega_market_core.data_generator import INITIAL_AMOUNT, MAX_DAILY_TRANSACTION
from mega_market_core.models import Item, TargetUser, Geo, Buy, Sell


@shared_task
def create_random_user_accounts():
    for i in range(0, MAX_DAILY_TRANSACTION):
        target_user_amount = TargetUser.objects.all().count()
        item_amount = Item.objects.all().count()
        geo_amount = Geo.objects.all().count()

        target_user_amount_id = randrange(0, target_user_amount) + 1
        temp_item_id = randrange(0, item_amount) + 1
        temp_geo_id = randrange(0, geo_amount) + 1

        transaction_amount = randrange(INITIAL_AMOUNT * 0.1, INITIAL_AMOUNT * 0.9)
        transaction_price = Item(id=temp_item_id).generate_next_price()

        random_days = randrange(0, 30)
        day = datetime(2000, 1, 1, 0, 0, 0) + timedelta(days=random_days)

        if randrange(0, 2):
            temp_transaction = Buy(
                item_id=temp_item_id,
                amount=transaction_amount,
                unit_price=transaction_price,
                date=day,
                target_user_id=target_user_amount_id,
                geo_id=temp_geo_id,
            )
        else:
            temp_transaction = Sell(
                item_id=temp_item_id,
                amount=transaction_amount,
                unit_price=transaction_price,
                date=day,
                target_user_id=target_user_amount_id,
                geo_id=temp_geo_id,
            )

        logging.warning(temp_transaction)
        try:
            temp_transaction.save()
        except Exception as e:
            logging.error(e)
            logging.error('item_id %s' % temp_transaction.item)
            logging.error('item %s' % temp_transaction.item)
            logging.error('type %s' % temp_transaction.type)
            logging.error('amount %s' % temp_transaction.amount)
            logging.error('unit_price %s' % temp_transaction.unit_price)
            logging.error('date %s' % temp_transaction.date)
            logging.error('target_user %s' % temp_transaction.target_user)
            logging.error('geo_id %s' % temp_transaction.geo)
    return '{} random transactions created with success!'.format(i)