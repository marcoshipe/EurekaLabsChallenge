import pytest
from unittest import mock
from app.api_integrations.alphavantage import get_stock_market_data
from app.api_integrations.api_integration_exceptions import ApiCallException
from app.misc.mocks import MockRequestsResponse


class TestAlphavantage:
    def test_ok_not_ordered(self):
        request_response_json = {
            'Time Series (Daily)': {
                '2022-10-20': {
                    '1. open': '2', '2. high': '2', '3. low': '2', '4. close': '2', '5. volume': '2345'
                },
                '2022-10-19': {
                    '1. open': '3.1', '2. high': '3.2', '3. low': '2.9', '4. close': '3.12', '5. volume': '3456'
                },
                '2022-10-18': {
                    '1. open': '4.1', '2. high': '4.22', '3. low': '2.9', '4. close': '3.04'
                },
                '2022-10-21': {
                    '1. open': '1', '2. high': '1', '3. low': '1', '4. close': '1', '5. volume': '12345'
                },
            }
        }
        expected_result = {
            '2022-10-21': {
                'open_price': '1', 'higher_price': '1', 'lower_price': '1',
                'close_price_diff_with_one_previous_day': '-1', 'close_price_diff_with_two_previous_days': '-2.12'
            },
            '2022-10-20': {
                'open_price': '2', 'higher_price': '2', 'lower_price': '2',
                'close_price_diff_with_one_previous_day': '-1.12', 'close_price_diff_with_two_previous_days': '-1.04'
            },
            '2022-10-19': {
                'open_price': '3.1', 'higher_price': '3.2', 'lower_price': '2.9',
                'close_price_diff_with_one_previous_day': '0.08', 'close_price_diff_with_two_previous_days': ''
            },
            '2022-10-18': {
                'open_price': '4.1', 'higher_price': '4.22', 'lower_price': '2.9',
                'close_price_diff_with_one_previous_day': '', 'close_price_diff_with_two_previous_days': ''
            }
        }
        with mock.patch('requests.get', mock.Mock(return_value=MockRequestsResponse(200, request_response_json))):
            assert get_stock_market_data('TEST') == expected_result

    @mock.patch('requests.get', mock.Mock(return_value=MockRequestsResponse(401, None)))
    def test_http_status_not_ok(self):
        with pytest.raises(ApiCallException, match='There was an error trying to get the stock data. Try again in a '
                                                   'few minutes'):
            get_stock_market_data('TEST')

    @mock.patch('requests.get', mock.Mock(return_value=MockRequestsResponse(200, raise_json_exception=True)))
    def test_body_is_not_json(self):
        with pytest.raises(ApiCallException, match='There was an error trying to get the stock data. Try again in a '
                                                   'few minutes'):
            get_stock_market_data('TEST')

    @mock.patch('requests.get', mock.Mock(return_value=MockRequestsResponse(200, {'Error Message': 'error'})))
    def test_error_in_json(self):
        with pytest.raises(ApiCallException, match='There was an error trying to get the stock data. Check if the '
                                                   'stock symbol is correct and try again in a few minutes'):
            get_stock_market_data('TEST')

    @mock.patch('requests.get', mock.Mock(return_value=MockRequestsResponse(200, {'Time Series (Daily': {}})))
    def test_invalid_json_key_not_found(self):
        with pytest.raises(ApiCallException, match='There was an error trying to get the stock data. Try again in a '
                                                   'few minutes'):
            get_stock_market_data('TEST')

    @mock.patch('requests.get', mock.Mock(return_value=MockRequestsResponse(200, {'Time Series (Daily)': 1})))
    def test_invalid_json_invalid_type(self):
        with pytest.raises(ApiCallException, match='There was an error trying to get the stock data. Try again in a '
                                                   'few minutes'):
            get_stock_market_data('TEST')

    def test_invalid_json_invalid_decimal(self):
        request_response_json = {
            'Time Series (Daily)': {'2022-10-21': {'1. open': '1', '2. high': '1', '3. low': '1', '4. close': 'A'}}
        }
        with mock.patch('requests.get', mock.Mock(return_value=MockRequestsResponse(200, request_response_json))):
            with pytest.raises(ApiCallException, match='There was an error trying to get the stock data. Try again in '
                                                       'a few minutes'):
                get_stock_market_data('TEST')
