import datetime
import logging
import redis
from fastapi import APIRouter, Response, status, Path, Depends, Header
from sqlalchemy.orm import Session
from app.config import settings
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
    429: {
        'description': 'Too Many Requests',
        'content': {'application/json': {'example': {
            'detail': 'The limit of 10 requests per minute was exceeded'
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
    logger = logging.getLogger('default')
    logger.info('Calling to stock_market_data with stock_symbol: %s', stock_symbol)
    if get_user_by_apikey(db, api_key) is None:
        logger.info('    Unauthorized, invalid api_key')
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'detail': 'invalid api_key'}

    # Check throttling
    cache = redis.Redis(host=settings.redis, port=6379)
    if len(cache.keys(api_key+'sec*')) >= 1:
        response.status_code = status.HTTP_429_TOO_MANY_REQUESTS
        return {'details': 'The limit of 1 request per second was exceeded'}
    if len(cache.keys(api_key+'min*')) >= 10:
        response.status_code = status.HTTP_429_TOO_MANY_REQUESTS
        return {'details': 'The limit of 10 requests per minute was exceeded'}
    cache.set(api_key+'sec'+str(datetime.datetime.now().timestamp()), '', 1)
    cache.set(api_key + 'min' + str(datetime.datetime.now().timestamp()), '', 60)

    try:
        result = get_stock_market_data(stock_symbol)
        logger.info('    Result: %s', result)
        return result
    except ApiCallException as e:
        logger.exception('    There was a problem trying to get the stock market data')
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {'detail': str(e)}
