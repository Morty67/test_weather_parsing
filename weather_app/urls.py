from django.urls import path, register_converter

from weather_app.utils.date_converter import DateConverter
from weather_app.views import WeatherView, WeatherRunView

register_converter(DateConverter, "date")

urlpatterns = [
    path("weather/<date:date>/", WeatherView.as_view(), name="weather"),
    path("weather/run/", WeatherRunView.as_view(), name="weather-run"),
]

app_name = "weather"
