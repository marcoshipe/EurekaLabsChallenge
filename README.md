# Resolution of the Stock Market API Service challenge
Problem definition: https://github.com/eurekalabs-io/challenges/blob/main/backend/python/stock-market-service.md

## Local deploy:
* Before the next steps you need an OS with `docker` and `docker-compose` installed

* Clone the repository:

  > git clone git@github.com:marcoshipe/EurekaLabsChallenge.git

* Go to the project folder:

  > cd EurekaLabsChallenge

* Copy the `env_template` file to `.env` and replace the `REPLACE_WITH_THE_ALPHAVANTAGE_APIKEY` with the real 
 alpha vantage api key. It is not mandatory, but you can edit the postgres settings, the SECRET_KEY and the SALT too

* Run the project in a container:

  > docker-compose up app

* To run the tests:

  > docker-compose up app_test

* To read the endpoint documentation and make calls to them (with the project container running): visit the webpage 
http://127.0.0.1:8080/docs

* The logs of the endpoints calls are saved in the folder `app/logs` in a maximum of 5 files of 100mb each. The logs of the server are saved in `app.log`, `app.log.1`, ... and the logs of the tests in `app_test.log`, `app_test.log.1`, ...

* A server to test the endpoints will be available in my raspberry pi (not 100% guaranteed because I'm traveling these days and I'm taking the raspberry with me) in: https://a7fc-45-173-17-217.sa.ngrok.io/docs
