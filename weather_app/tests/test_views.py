from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from weather_app.views import WeatherRunView


class WeatherRunViewTestCase(TestCase):
    def test_run_parser_on_post_request(self):
        # Creating a query factory instance.
        factory = APIRequestFactory()

        # Creating a POST request.
        url = "/weather/run/"
        request = factory.post(url)

        # Calling a view (endpoint).
        response = WeatherRunView.as_view()(request)

        # Checking the response status and message.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Weather information updated."
        )
