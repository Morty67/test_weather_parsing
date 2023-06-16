import requests
import schedule
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_parsing.settings")
django.setup()

from weather_app.models import Weather, ParserTimeSettings

CITY = "Kyiv"
BASE_URL = f"https://pogoda.meta.ua/ua/Kyivska/Kyivskiy/{CITY}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/114.0.5735.111 Safari/537.36",
}
TIME_TO_PARSE = "09:00"


class TaskStatus:
    """A class that defines constants representing different statuses for a
    task."""

    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class WeatherData:
    """A class that represents weather data for a specific date, including
    date, temperature, and description."""

    def __init__(self, date, temperature, description):
        self.date = date
        self.temperature = temperature
        self.description = description


class WeatherParser:
    """A class responsible for parsing weather data from a website based on
    a given date."""

    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def parse_weather(self, date, time_to_parse):
        try:
            response = requests.get(
                f"{self.base_url}/{date}/ajax/", headers=self.headers
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            forecast_items = soup.find_all("div", class_="city__forecast-col")
            for item in forecast_items:
                time = item.find(
                    "div", class_="city__forecast-time"
                ).text.strip()
                temperature = item.find(
                    "span", class_="graph-data__value"
                ).text.strip()
                if time == time_to_parse:
                    description_div = item.find(
                        "div", class_="city__forecast-icon"
                    )
                    description = description_div["data-tippy-content"]
                    return WeatherData(date, temperature, description)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {e}")

        return None


class WeatherSaver:
    """A class that handles saving weather data to the database using the
    Weather model"""

    def save_weather(self, date, temperature, description):
        Weather.objects.update_or_create(
            date=date,
            defaults={
                "temperature": temperature,
                "weather_description": description,
            },
        )


def update_task_status(status):
    """A function that prints and updates the status of the parsing task."""
    print(f"Parser status: {status}")


def parse_weather_for_date(base_url, date, time_to_parse):
    """A function that orchestrates the parsing of weather data for a
    specific date."""
    update_task_status(TaskStatus.IN_PROGRESS)

    print(f"Parsing weather for a specific date: {date}")

    parser = WeatherParser(base_url, HEADERS)
    saver = WeatherSaver()

    weather_data = parser.parse_weather(date, time_to_parse)
    if weather_data:
        saver.save_weather(
            weather_data.date,
            weather_data.temperature,
            weather_data.description,
        )

    print(f"Weather parsing for the specified date is complete: {date}")
    update_task_status(TaskStatus.DONE)
    print()


def parse_weather_for_days(base_url, num_days: int = 6, time_to_parse=TIME_TO_PARSE):
    """A function that iterates over a specified number of days and calls
    parse_weather_for_date for each day."""
    current_date = datetime.now().date()
    parser = WeatherParser(base_url, HEADERS)
    saver = WeatherSaver()

    for i in range(num_days):
        date = (current_date + timedelta(days=i)).strftime("%Y-%m-%d")
        parse_weather_for_date(base_url, date, time_to_parse)


def run_parser():
    """A function that calls parse_weather_for_days to initiate the parsing
    process for a default number of days."""

    update_task_status(TaskStatus.SCHEDULED)

    while True:
        # Check if ParserTimeSettings object exists
        if ParserTimeSettings.objects.exists():
            parser_time_settings = ParserTimeSettings.objects.last()
            time_to_parse = parser_time_settings.parser_time
        else:
            time_to_parse = TIME_TO_PARSE

        parse_weather_for_days(BASE_URL, time_to_parse=time_to_parse)

        # Schedule next run based on the selected time
        schedule.every().day.at(time_to_parse).do(run_parser)

        schedule.run_pending()
        time.sleep(360)


if __name__ == "__main__":
    """The main entry point of the script. It calls run_parser initially and 
    sets up a schedule to run run_parser daily at a specific time."""
    run_parser()
