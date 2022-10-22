import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers import stock_market_data


app_description = """
Resolution of the Stock Market API Service challenge

[Problem definition](https://github.com/eurekalabs-io/challenges/blob/main/backend/python/stock-market-service.md)

## Stock market data

Get daily time series about a stock
"""

app = FastAPI(title='Eureka Labs Challenge', description=app_description)
app.include_router(stock_market_data.router)


# Code to remove the 422 response in the docs for specifics endpoints
def custom_openapi():
    endpoints_to_remove = [('/stock_market_data/{stock_symbol}', 'get')]
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for endpoint_to_remove in endpoints_to_remove:
            del app.openapi_schema.get('paths')[endpoint_to_remove[0]][endpoint_to_remove[1]]['responses']['422']
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
