from django import forms

from mega_market_core.models import Buy


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields = ('amount', 'unit_price', 'date', 'target_user', 'geo', 'item')
