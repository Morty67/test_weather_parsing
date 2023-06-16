from django.test import TestCase
from rest_framework.exceptions import ValidationError

from weather_app.models import Weather


class WeatherTestCase(TestCase):
    def test_valid_temperature(self):
        # Validating the permissible temperature.
        weather = Weather(
            date="2023-06-16", temperature=25, weather_description="Sunny"
        )
        try:
            weather.full_clean()  # Triggering the validation.
        except ValidationError:
            self.fail("Validation error occurred for valid temperature")

    def test_invalid_temperature(self):
        # Checking the validation of an invalid temperature.
        weather = Weather(
            date="2023-06-17", temperature=100, weather_description="Hot"
        )
        with self.assertRaises(ValidationError):
            weather.full_clean()  # Expecting a ValidationError exception.

    def test_update_or_create_existing_object(self):
        # Updating an existing Weather object.
        existing_weather = Weather.objects.create(
            date="2023-06-16", temperature=25, weather_description="Sunny"
        )
        updated_temperature = 30
        updated_description = "Partly cloudy"

        updated_weather = Weather.update_or_create(
            date="2023-06-16",
            temperature=updated_temperature,
            weather_description=updated_description,
        )

        self.assertEqual(updated_weather.temperature, updated_temperature)
        self.assertEqual(
            updated_weather.weather_description, updated_description
        )
        self.assertEqual(updated_weather.id, existing_weather.id)

    def test_update_or_create_new_object(self):
        # Creating a new Weather object.
        date = "2023-06-18"
        temperature = 28
        description = "Warm and sunny"

        new_weather = Weather.update_or_create(
            date=date,
            temperature=temperature,
            weather_description=description,
        )

        self.assertEqual(new_weather.temperature, temperature)
        self.assertEqual(new_weather.weather_description, description)
        self.assertEqual(new_weather.date, date)
        self.assertIsNotNone(new_weather.id)
