from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from mega_market_core.models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('type', 'amount', 'unit_price', 'date', 'target_user', 'geo', 'item')
