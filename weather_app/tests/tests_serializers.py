from django.test import TestCase
from datetime import date

from rest_framework.exceptions import ValidationError

from weather_app.models import Weather
from weather_app.serializers import WeatherSerializer


class WeatherSerializerTestCase(TestCase):
    def test_serialization(self):
        # Creating a Weather object.
        weather = Weather.objects.create(
            date=date(2023, 6, 16),
            temperature=25,
            weather_description="Sunny",
        )

        # Serializing the Weather object.
        serializer = WeatherSerializer(weather)

        # Checking the serialized data.
        expected_data = {
            "date": "16.06.2023",
            "temperature": 25,
            "weather_description": "Sunny",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_deserialization(self):
        # Input data for deserialization.
        data = {
            "date": "2023-06-16",
            "temperature": 25,
            "weather_description": "Sunny",
        }

        # Deserializing the data.
        serializer = WeatherSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        deserialized_data = serializer.validated_data

        # Checking the deserialized data.
        expected_date = date(2023, 6, 16)
        self.assertEqual(deserialized_data["date"], expected_date)
        self.assertEqual(deserialized_data["temperature"], 25)
        self.assertEqual(deserialized_data["weather_description"], "Sunny")

    def test_deserialization_invalid_data(self):
        # Input data for invalid deserialization.
        data = {
            "date": "16-06-2023",
            "temperature": "1.25",
            # Invalid temperature value (string instead of a number).
            "weather_description": "Sunny",
        }

        # Deserializing the data.
        serializer = WeatherSerializer(data=data)

        # Expecting a ValidationError exception during invalid deserialization.
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_deserialization_missing_required_fields(self):
        # Input data with a missing required field.
        data = {"temperature": 25, "weather_description": "Sunny"}

        # Deserializing the data.
        serializer = WeatherSerializer(data=data)

        # Expecting a ValidationError exception during invalid deserialization.
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
