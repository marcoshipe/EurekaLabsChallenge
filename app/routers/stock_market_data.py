from fastapi import APIRouter, Response, status, Path, Depends, Header
from sqlalchemy.orm import Session
from app.api_integrations.alphavantage import get_stock_market_data
from app.api_integrations.api_integration_exceptions import ApiCallException
from app.crud.crud_user import get_user_by_apikey
from app.database.database import get_db


router = APIRouter(prefix='/stock_market_data', tags=['Stock market data'])

responses = {
    200: {
        'description': 'Successful Response',
        'content': {'application/json': {'example': {
            '2022-06-03': {
                'open_price': '140.2600',
                'higher_price': '142.5794',
                'lower_price': '139.7400',
                'close_price_diff_with_one_previous_day': '1.0300',
                'close_price_diff_with_two_previous_days': '1.7500'
            },
            '2022-06-02': {
                'open_price': '139.4500',
                'higher_price': '140.2900',
                'lower_price': '136.8500',
                'close_price_diff_with_one_previous_day': '0.7200',
                'close_price_diff_with_two_previous_days': ''
            },
            '2022-06-01': {
                'open_price': '139.6700',
                'higher_price': '140.4699',
                'lower_price': '138.5200',
                'close_price_diff_with_one_previous_day': '',
                'close_price_diff_with_two_previous_days': ''
            }
        }}}
    },
    401: {
        'description': 'Unauthorized',
        'content': {'application/json': {'example': {
            'detail': 'invalid api_key'
        }}}
    },
    503: {
        'description': 'Service unavailable',
        'content': {'application/json': {'example': {
            'detail': 'There was an error trying to get the stock data. Try again in a few minutes'
        }}}
    },
}


@router.get('/{stock_symbol}', responses=responses, summary='Get Stock Market Data')
def get_stock_market_data_api(response: Response, stock_symbol: str = Path(example='IBM'), api_key: str = Header(),
                              db: Session = Depends(get_db)):
    if get_user_by_apikey(db, api_key) is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'detail': 'invalid api_key'}
    try:
        return get_stock_market_data(stock_symbol)
    except ApiCallException as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {'detail': str(e)}
