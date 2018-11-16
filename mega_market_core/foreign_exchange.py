import logging
from datetime import datetime, timedelta

import requests
from django.core.cache import cache

from MegaMarket.celery import ONE_DAY_IN_SECONDS
from MegaMarket.settings import EXCHANGE_RATE_API_KEY

EXAMPLE_EXCHANGE_RATE = {'result': 'success', 'timestamp': 1542210490, 'from': 'USD',
                         'rates': {'USD': 1, 'AED': 3.6727, 'ALL': 110.1, 'AMD': 487.46, 'ANG': 1.785, 'AOA': 309.916,
                                   'ARS': 36.13, 'AUD': 1.38600901, 'AZN': 1.6995, 'BBD': 2.0, 'BDT': 83.79,
                                   'BGN': 1.73679586, 'BHD': 0.3767, 'BRL': 3.78098081, 'BSD': 1.0, 'BWP': 10.7593,
                                   'BYN': 2.12, 'CAD': 1.32339537, 'CHF': 1.00823127, 'CLP': 685.76, 'CNY': 6.95407019,
                                   'COP': 3186.2, 'CZK': 22.98725051, 'DKK': 6.60659578, 'DOP': 50.06, 'DZD': 118.498,
                                   'EGP': 17.88, 'ETB': 27.7, 'EUR': 0.88519462, 'FJD': 2.116, 'GBP': 0.77038477,
                                   'GEL': 2.7055, 'GHS': 4.7908, 'GNF': 9040.0, 'GTQ': 7.694, 'HKD': 7.83064658,
                                   'HNL': 24.142, 'HRK': 6.56533602, 'HUF': 285.73260704, 'IDR': 14822.91234062,
                                   'ILS': 3.6911979, 'INR': 72.50142689, 'IQD': 1190.0, 'IRR': 42000.0,
                                   'ISK': 124.22323273, 'JMD': 125.82, 'JOD': 0.7085, 'JPY': 113.92025108,
                                   'KES': 102.45, 'KHR': 4001.6, 'KRW': 1132.14725541, 'KWD': 0.3039, 'KZT': 374.92,
                                   'LAK': 8543.0, 'LBP': 1508.0, 'LKR': 175.9, 'MAD': 9.5247, 'MDL': 16.929,
                                   'MKD': 54.11, 'MMK': 1603.0, 'MUR': 34.65, 'MXN': 20.42086309, 'MYR': 4.19418763,
                                   'NAD': 14.287, 'NGN': 363.0, 'NOK': 8.48365718, 'NZD': 1.47740827, 'OMR': 0.3846,
                                   'PAB': 1.0, 'PEN': 3.37567596, 'PGK': 3.3645, 'PHP': 53.10740584, 'PKR': 132.52,
                                   'PLN': 3.8022558, 'PYG': 5925.1, 'QAR': 3.6403, 'RON': 4.12150171, 'RSD': 104.4847,
                                   'RUB': 67.60352924, 'SAR': 3.75120402, 'SCR': 13.56, 'SEK': 9.07271769,
                                   'SGD': 1.38043099, 'THB': 32.97632731, 'TJS': 9.4191, 'TND': 2.91, 'TRY': 5.48639299,
                                   'TTD': 6.679, 'TWD': 30.88235508, 'TZS': 2292.0, 'UAH': 27.7945, 'UYU': 32.7,
                                   'UZS': 8261.0, 'VEF': 248209.0, 'VND': 23271.27774965, 'XAF': 578.27, 'XCD': 2.7,
                                   'XOF': 578.27, 'XPF': 104.92, 'ZAR': 14.38888616, 'ZMW': 11.88}}


def get_exchange_rate_dictionary():
    forex_dictionary = cache.get('foreign_exchange_dictionary')
    forex_request_timestamp = datetime.utcfromtimestamp(int(forex_dictionary['timestamp']))
    yesterday = datetime.now() - timedelta(days=1)

    if (forex_request_timestamp <= yesterday) | (forex_dictionary is None):
        url = 'https://v3.exchangerate-api.com/bulk/' + EXCHANGE_RATE_API_KEY + '/USD'
        # Making our request
        response = requests.get(url)
        forex_dictionary = response.json()
        # Your JSON object
        logging.debug(forex_dictionary)
        cache.set('foreign_exchange_dictionary', forex_dictionary, ONE_DAY_IN_SECONDS)

    return forex_dictionary
