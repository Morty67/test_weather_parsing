import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import schedule
import time
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_parsing.settings")
django.setup()

from weather_app.models import Weather

CITY = "Kyiv"
BASE_URL = f"https://pogoda.meta.ua/ua/Kyivska/Kyivskiy/{CITY}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.111 Safari/537.36",
}
TIME_TO_PARSE = "09:00"


class TaskStatus:
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class WeatherData:
    def __init__(self, date, temperature, description):
        self.date = date
        self.temperature = temperature
        self.description = description


class WeatherParser:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def parse_weather(self, date):
        try:
            response = requests.get(f"{self.base_url}/{date}/ajax/",
                                    headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            forecast_items = soup.find_all("div", class_="city__forecast-col")
            for item in forecast_items:
                time = item.find("div",
                                 class_="city__forecast-time").text.strip()
                temperature = item.find("span",
                                        class_="graph-data__value").text.strip()
                if time == TIME_TO_PARSE:
                    description_div = item.find("div",
                                                class_="city__forecast-icon")
                    description = description_div["data-tippy-content"]
                    return WeatherData(date, temperature, description)

        except requests.exceptions.RequestException as e:
            print(f"Виникла помилка при запиті: {e}")

        return None


class WeatherSaver:
    def save_weather(self, date, temperature, description):
        Weather.objects.update_or_create(
            date=date,
            defaults={
                "temperature": temperature,
                "weather_description": description,
            },
        )


def update_task_status(status):
    print(f"Статус парсера: {status}")


def parse_weather_for_date(base_url, date):
    update_task_status(TaskStatus.IN_PROGRESS)

    print(f"Парсинг погоди для дати: {date}")

    parser = WeatherParser(base_url, HEADERS)
    saver = WeatherSaver()

    weather_data = parser.parse_weather(date)
    if weather_data:
        saver.save_weather(weather_data.date, weather_data.temperature,
                           weather_data.description)

    print(f"Завершено парсинг погоди для дати: {date}")
    update_task_status(TaskStatus.DONE)
    print()


def parse_weather_for_days(base_url, num_days: int = 6):
    current_date = datetime.now().date()
    parser = WeatherParser(base_url, HEADERS)
    saver = WeatherSaver()

    for i in range(num_days):
        date = (current_date + timedelta(days=i)).strftime("%Y-%m-%d")
        parse_weather_for_date(base_url, date)


def run_parser():
    parse_weather_for_days(BASE_URL)


if __name__ == "__main__":
    run_parser()

    schedule.every().day.at(TIME_TO_PARSE).do(run_parser)

    update_task_status(TaskStatus.SCHEDULED)

    while True:
        schedule.run_pending()
        time.sleep(360)
