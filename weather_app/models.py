from django.db import models
from rest_framework.exceptions import ValidationError


class Weather(models.Model):
    date = models.DateField(unique=True)
    temperature = models.IntegerField()
    weather_description = models.TextField()

    def __str__(self):
        return str(self.date)

    def clean(self):
        """ It checks if the temperature value falls within the acceptable
        range of -60 to +70"""
        super().clean()
        if not (-60 <= self.temperature <= 70):
            raise ValidationError("Temperature must be between -60 and +70.")

    @classmethod
    def update_or_create(cls, date, temperature, weather_description):
        """ It is used to update an existing Weather object or create a new
        one if it doesn't exist."""
        try:
            weather = cls.objects.get(date=date)
            weather.temperature = temperature
            weather.weather_description = weather_description
            weather.save()
        except cls.DoesNotExist:
            weather = cls.objects.create(date=date, temperature=temperature,
                                         weather_description=weather_description)
        return weather


class ParserTimeSettings(models.Model):
    parser_time = models.CharField(max_length=5)

    def __str__(self):
        return self.parser_time
