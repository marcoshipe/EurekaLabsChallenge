# Resolution of the Stock Market API Service challenge
Problem definition: https://github.com/eurekalabs-io/challenges/blob/main/backend/python/stock-market-service.md

## Local deploy:
* Before the next steps you need an OS with `docker` and `docker-compose` installed

* Clone the repository:

  > git clone git@github.com:marcoshipe/EurekaLabsChallenge.git

* Go to the project folder:

  > cd EurekaLabsChallenge

* Copy the `env_template` file to `.env` and replace the `REPLACE_WITH_THE_ALPHAVANTAGE_APIKEY` with the real 
 alpha vantage api key. It is not mandatory, but you can edit the postgres settings too

* Run the project in a container:

  > docker-compose up app

* To run the tests:

  > docker-compose up app_test

* To read the endpoint documentation and make calls to them (with the project container running): visit the webpage 
http://127.0.0.1:8080/docs