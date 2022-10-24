import sys
import uvicorn
from fastapi import FastAPI
from app.routers import stock_market_data, users
from app.database.database import engine
from app.database.setup_teardown import setup_db


app_description = '''
Resolution of the Stock Market API Service challenge

[Problem definition](https://github.com/eurekalabs-io/challenges/blob/main/backend/python/stock-market-service.md)

## Stock market data

Get daily time series about a stock
'''


if 'pytest' not in sys.modules:
    setup_db(engine)
app = FastAPI(title='Eureka Labs Challenge', description=app_description)
app.include_router(stock_market_data.router)
app.include_router(users.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
