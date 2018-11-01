from random import randrange, getrandbits

from django.db import models
from django.db.models import Sum, ExpressionWrapper, F

COUNTRY_CHOICES = (('URUGUAY', 'Uruguay'),)
relative_maximum_percent_range = 20  # Integers percentage numbers only

CHART_DATE_FORMAT_FOR_DATETIME = "%Y-%m-%d"
CHART_DATE_FORMAT_FOR_AMCHARTS = "YYYY-MM-DD"


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
            last_unit_price = self.transactions.all().order_by('date').reverse()[0].unit_price
        except Exception as e:
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


class Transaction(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    # The type sign is defined accordingly to the money interpretation of the transaction, if it is a buy transaction
    # the money is used to pay so it goes away from our funds so it is a negative transaction.
    TRANSACTION_TYPE_CHOICES = ((BUY, -1), (SELL, 1))

    type = models.CharField(max_length=5, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.IntegerField()
    unit_price = models.FloatField()
    date = models.DateTimeField()
    target_user = models.ForeignKey(TargetUser, related_name="transactions", on_delete=models.PROTECT)
    geo = models.ForeignKey(Geo, related_name="transactions", on_delete=models.PROTECT)
    item = models.ForeignKey(Item, related_name="transactions", on_delete=models.PROTECT)

    # def save(self, *args, **kwargs):
    #     item = self.item
    #     item.stock += self.amount * self.type * -1  # the -1 is because the stock and the money transaction are opposites
    #     item.save()
    #     super(Transaction, self).save(*args, **kwargs)

    def get_bought_list_by_date_filtered(**kargs):
        filters = kargs
        bought_list = Transaction.objects.filter(**filters, type=Transaction.BUT).values('date').annotate(
            data_sum=ExpressionWrapper(
                Sum(F('unit_price') * F('amount')), output_field=models.FloatField()
            )
        ).order_by('date')

        for day in bought_list:
            day['date'] = day['date'].strftime(CHART_DATE_FORMAT_FOR_DATETIME)
        return bought_list



    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.id, self.item.name, str(self.date), self.amount, self.unit_price)


class Buy(models.Model):
    amount = models.IntegerField()
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
        bought_list = Buy.objects.filter(**filters).values('date').annotate(
            data_sum=ExpressionWrapper(
                Sum(F('unit_price') * F('amount')), output_field=models.FloatField()
            )
        ).order_by('date')

        for day in bought_list:
            day['date'] = day['date'].strftime(CHART_DATE_FORMAT_FOR_DATETIME)
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
        sold_list = Sell.objects.filter(**filters).values('date').annotate(
            data_sum=ExpressionWrapper(
                Sum(F('unit_price') * F('amount')), output_field=models.FloatField()
            )
        ).order_by('date')

        for day in sold_list:
            day['date'] = day['date'].strftime(CHART_DATE_FORMAT_FOR_DATETIME)
        return sold_list

    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.id, self.item.name, str(self.date), self.amount, self.unit_price)

#
#     Query para sacar ganancias usando transaction igual para Buy y Sell y la suma se podria hacer la grafica
# Transaction.objects.filter(**filters).values('date').annotate(data_sum=Sum('amount')).order_by('date')
#
#
# Buy.objects.filter(**filters).values('date').annotate(data_sum=Sum('amount')).order_by('date')
# Sell.objects.filter(**filters).values('date').annotate(data_sum=Sum('amount')).order_by('date')
#
