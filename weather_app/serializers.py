from rest_framework import serializers

from weather_app.models import Weather, ParserTimeSettings


class WeatherSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = Weather
        fields = ["date", "temperature", "weather_description"]


class ParserTimeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParserTimeSettings
        fields = ["parser_time"]
