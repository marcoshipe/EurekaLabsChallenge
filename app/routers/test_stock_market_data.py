from unittest import mock
from fastapi.testclient import TestClient
from app.main import app
from app.api_integrations.api_integration_exceptions import ApiCallException


class TestMarketData:
    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)

    def test_ok(self):
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
        with mock.patch('app.routers.stock_market_data.get_stock_market_data', mock.Mock(return_value=expected_result)):
            response = self.client.get("/stock_market_data/TEST")
        assert response.status_code == 200
        assert response.json() == expected_result

    def test_exception(self):
        exception_message = 'There was an error trying to get the stock data. Try again in a few minutes'
        with mock.patch('app.routers.stock_market_data.get_stock_market_data',
                        mock.Mock(side_effect=ApiCallException(exception_message))):
            response = self.client.get("/stock_market_data/TEST")
        assert response.status_code == 503
        assert response.json() == {'error': exception_message}
