from rest_framework import serializers

from weather_app.models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d.%m.%Y")

    class Meta:
        model = Weather
        fields = ["date", "temperature", "weather_description"]
