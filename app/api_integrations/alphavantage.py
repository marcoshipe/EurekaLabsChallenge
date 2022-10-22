import requests
from decimal import Decimal, InvalidOperation
from requests import JSONDecodeError
from app.api_integrations.api_integration_exceptions import ApiCallException
from app.config import settings


def get_stock_market_data(stock_symbol: str) -> dict:
    """ Get stock market data from alpha vantage and return it as a dict with this structure:
    {
        'yyyy-mm-dd': {
            'open_price': decimal string,
            'higher_price': decimal string,
            'lower_price': decimal string,
            'close_price_diff_with_one_previous_day': decimal string or empty string if there is not a previous day,
            'close_price_diff_with_two_previous_days': decimal string or empty string if there are not two previous days
        },
        ...
    }

    :param stock_symbol: symbol of the stock you want to get the data
    :return: dict
    """
    response = requests.get(settings.alphavantage_url, params={
        'function': 'TIME_SERIES_DAILY',
        'outputsize': 'compact',
        'apikey': settings.alphavantage_apikey,
        'symbol': stock_symbol,
    })

    if response.status_code != 200:
        raise ApiCallException('There was an error trying to get the stock data. Try again in a few minutes')

    try:
        response_json = response.json()
    except JSONDecodeError:
        raise ApiCallException('There was an error trying to get the stock data. Try again in a few minutes')
    if 'Error Message' in response_json:
        raise ApiCallException('There was an error trying to get the stock data. Check if the stock symbol is correct '
                               'and try again in a few minutes')
    try:
        stock_market_data = {}
        close_prev = None
        close_prev2 = None
        for date, daily_data in sorted(response_json['Time Series (Daily)'].items()):
            close_price_diff_with_prev = '{0:f}'.format(Decimal(daily_data['4. close']) - close_prev) \
                if close_prev is not None else ''
            close_price_diff_with_prev2 = '{0:f}'.format(Decimal(daily_data['4. close']) - close_prev2) \
                if close_prev2 is not None else ''
            stock_market_data[date] = {
                'open_price': daily_data['1. open'],
                'higher_price': daily_data['2. high'],
                'lower_price': daily_data['3. low'],
                'close_price_diff_with_one_previous_day': close_price_diff_with_prev,
                'close_price_diff_with_two_previous_days': close_price_diff_with_prev2,
            }
            close_prev2 = close_prev
            close_prev = Decimal(daily_data['4. close'])
    except (KeyError, AttributeError, InvalidOperation, ValueError):
        raise ApiCallException('There was an error trying to get the stock data. Try again in a few minutes')
    return dict(sorted(stock_market_data.items(), reverse=True))
