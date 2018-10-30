from django.shortcuts import render, redirect
from django.urls import reverse

from mega_market_core.forms import TransactionForm

GET = 'GET'
POST = 'POST'


def dashboard(request):
    """
    View used for the dashboard page with the ticket to add more transactions
    :param request:
    :return:
    """

    if request.method == GET:
        form = TransactionForm()
        return render(request, 'dashboard.html', {'form': form})

    elif request.method == POST:
        form = TransactionForm(request.POST)
        template = 'dashboard.html'

    else:
        response = redirect(reverse('dashboard'))
        return response
