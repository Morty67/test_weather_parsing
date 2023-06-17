# Weather Parsing
An application that parses data from the website https://pogoda.meta.ua/en/Kyivska/Kyivskiy/Kyiv/ for the current day + 5 days.

## Installing / Getting started:
```shell
To get started, you need to clone the repository from GitHub: https://github.com/Morty67/test_weather_parsing
Python 3 must be installed

python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)

pip install -r requirements.txt

Your settings for DB in .env file:
POSTGRES_DB=<POSTGRES_DB>
POSTGRES_USER=<POSTGRES_USER>
POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
POSTGRES_HOST=<POSTGRES_HOST>
<SECRET_KEY>
SECRET_KEY=YOUR DJANGO SECRET KEY

python manage.py migrate
python manage.py runserver
```
## Run Docker 🐳
Docker must be installed 
```shell
*  docker-compose up --build
```
## How to get access

Domain:
*  localhost:8000 or 127.0.0.1:8000
* http://localhost:8000/api/weather/<date:date>/ (date in format like 16.06.2023)
* http://localhost:8000/api/weather/run/ (Run the parser through the endpoint)
* http://localhost:8000/api/parser-settings/ (Update-set parser startup time, format {
  "parser_time": "18:30"
})



## Features:

*  Admin panel - admin/
*  Documentation is located at api/doc/swagger/
*  An endpoint has been implemented to retrieve weather information through DRF.
*  The ability to change the weather information update time through the endpoint has been implemented.
*  Manual weather information update (task execution) has been implemented through the endpoint.
*  The ability to track the status of the parsing task (Scheduled, In Progress, Done) has been implemented.
