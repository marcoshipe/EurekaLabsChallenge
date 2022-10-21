# Resolution of the Stock Market API Service challenge
Problem definition: https://github.com/eurekalabs-io/challenges/blob/main/backend/python/stock-market-service.md

## Local deploy:
* Before the next steps you need an OS with `docker` and `docker-compose` installed

* Clone the repository:

  > git clone # TODO

* Go to the project folder:

  > cd EurekaLabsChallenge

* Copy the `env_template` file to `.env` and replace the `REPLACE_WITH_THE_ALPHAVANTAGE_APIKEY` with the real 
 alpha vantage api key

* Build the docker image:

  > docker-compose build

* Run the project in a container:

  > docker-compose up -d

* To run the tests (with the project container running):

  > docker-compose exec app pytest -v