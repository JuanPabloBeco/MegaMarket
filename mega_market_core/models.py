import logging
from random import randrange, getrandbits

from django.db import models
from django.db.models import Sum, ExpressionWrapper, F

COUNTRY_CHOICES = (('URUGUAY', 'Uruguay'),)
relative_maximum_percent_range = 20  # Integers percentage numbers only

CHART_DATE_FORMAT_FOR_DATETIME = "%Y-%m-%d"
CHART_DATE_FORMAT_FOR_AMCHARTS = "YYYY-MM-DD"

CHART_DATETIME_FORMAT_FOR_DATETIME = "%Y-%m-%d %H:%M:%S"
CHART_DATETIME_FORMAT_FOR_AMCHARTS = "YYYY-MM-DD JJ:mm:ss"


class Category(models.Model):
    name = models.CharField(max_length=100)


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name="sub_category", on_delete=models.CASCADE)


class Item(models.Model):
    name = models.CharField(max_length=100)
    sub_category = models.ForeignKey(SubCategory, related_name="items", on_delete=models.CASCADE)

    # stock = models.IntegerField()

    def get_last_unit_price(self):
        """
        This method gets the last price of this item or -1 if there is an error
        :return:
        """
        try:
            last_buy_unit_price = self.buy_transactions.all().order_by('-date').first()
            last_sell_unit_price = self.sell_transactions.all().order_by('-date').first()
            if last_sell_unit_price is None:
                last_unit_price = last_buy_unit_price.unit_price
            elif last_buy_unit_price.date > last_sell_unit_price.date:
                last_unit_price = last_buy_unit_price.unit_price
            else:
                last_unit_price = last_sell_unit_price.unit_price
        except Exception as e:
            logging.error(e)
            last_unit_price = -1
        return last_unit_price

    def generate_next_price(self):
        """
        This method generates a new unit price based on the last one
        :return:
        """
        last_price = self.get_last_unit_price()

        if last_price != -1:
            relative_percentage_range = randrange(0, int(relative_maximum_percent_range * 100)) / 100
            if getrandbits(1) == 1:
                relative_percentage_range = relative_percentage_range * -1
            new_price = round(last_price * (1 + relative_percentage_range / 100), 2)
            return new_price
        else:
            return -1


class Geo(models.Model):
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    city = models.CharField(max_length=100, null=True, blank=True, default='')


class TargetUser(models.Model):
    name = models.CharField(max_length=100)


class Buy(models.Model):
    amount = models.IntegerField()
    unit_price = models.FloatField()
    date = models.DateTimeField()
    target_user = models.ForeignKey(TargetUser, related_name="buy_transactions", on_delete=models.PROTECT)
    geo = models.ForeignKey(Geo, related_name="buy_transactions", on_delete=models.PROTECT)
    item = models.ForeignKey(Item, related_name="buy_transactions", on_delete=models.PROTECT)

    # def save(self, *args, **kwargs):
    #     item = self.item
    #     item.stock += self.amount * self.type * -1  # the -1 is because the stock and the money transaction are opposites
    #     item.save()
    #     super(Transaction, self).save(*args, **kwargs)

    def get_bought_list_by_date_filtered(**kargs):
        filters = kargs
        bought_list = Buy.objects.filter(
            **filters
        ).annotate(
            date_only=models.functions.Trunc('date', 'day')
        ).values(
            'date_only'
        ).annotate(
            data_sum=ExpressionWrapper(
                Sum(F('unit_price') * F('amount')), output_field=models.FloatField()
            )
        ).order_by('date_only')

        for day in bought_list:
            day['date'] = day.pop('date_only').strftime(CHART_DATE_FORMAT_FOR_DATETIME)
            day['data_sum'] = round(day['data_sum'], 2)
        return bought_list

    def get_bought_one_day_list_by_date_filtered(**kargs):
        filters = kargs
        bought_list = Buy.objects.filter(
            **filters
        ).annotate(
            date_only=models.functions.Trunc('date', 'hour')
        ).values(
            'date_only'
        ).annotate(
            data_sum=ExpressionWrapper(
                Sum(F('unit_price') * F('amount')), output_field=models.FloatField()
            )
        ).order_by(
            'date_only'
        )

        for day in bought_list:
            day['date'] = day.pop('date_only').strftime(CHART_DATETIME_FORMAT_FOR_DATETIME)
            day['data_sum'] = round(day['data_sum'], 2)
        return bought_list

    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.id, self.item.name, str(self.date), self.amount, self.unit_price)


class Sell(models.Model):
    amount = models.IntegerField()
    unit_price = models.FloatField()
    date = models.DateTimeField()
    target_user = models.ForeignKey(TargetUser, related_name="sell_transactions", on_delete=models.PROTECT)
    geo = models.ForeignKey(Geo, related_name="sell_transactions", on_delete=models.PROTECT)
    item = models.ForeignKey(Item, related_name="sell_transactions", on_delete=models.PROTECT)

    # def save(self, *args, **kwargs):
    #     item = self.item
    #     item.stock += self.amount * self.type * -1  # the -1 is because the stock and the money transaction are opposites
    #     item.save()
    #     super(Transaction, self).save(*args, **kwargs)

    def get_sold_list_by_date_filtered(**kargs):
        filters = kargs
        sold_list = Sell.objects.filter(
            **filters
        ).annotate(
            date_only=models.functions.Trunc('date', 'day')
        ).values('date_only').annotate(
            data_sum=ExpressionWrapper(
                Sum(F('unit_price') * F('amount')), output_field=models.FloatField()
            )
        ).order_by('date_only')

        for day in sold_list:
            day['date'] = day.pop('date_only').strftime(CHART_DATE_FORMAT_FOR_DATETIME)
            day['data_sum'] = round(day['data_sum'], 2)
        return sold_list

    def get_sold_one_day_list_by_date_filtered(**kargs):
        filters = kargs
        sold_list = Sell.objects.filter(
            **filters
        ).annotate(
            date_only=models.functions.Trunc('date', 'hour')
        ).values(
            'date_only'
        ).annotate(
            data_sum=ExpressionWrapper(
                Sum(F('unit_price') * F('amount')), output_field=models.FloatField()
            )
        ).order_by(
            'date_only'
        )

        for day in sold_list:
            day['date'] = day.pop('date_only').strftime(CHART_DATETIME_FORMAT_FOR_DATETIME)
            day['data_sum'] = round(day['data_sum'], 2)
        return sold_list

    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.id, self.item.name, str(self.date), self.amount, self.unit_price)
