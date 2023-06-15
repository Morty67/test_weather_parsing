from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from weather_parser import run_parser
from .models import Weather
from .serializers import WeatherSerializer


class WeatherView(generics.RetrieveAPIView):
    serializer_class = WeatherSerializer

    def get_object(self):
        date_str = self.kwargs["date"]
        try:
            return Weather.objects.get(date=date_str)
        except Weather.DoesNotExist:
            formatted_date = date_str.strftime("%d-%m-%Y")
            raise NotFound(
                f"Weather data for {formatted_date} does not exist."
            )
        except ValueError:
            raise NotFound(
                f"Invalid date format: {date_str}. Use the format 'dd.mm.yyyy'."
            )


class WeatherRunView(APIView):
    def post(self, request, format=None):
        run_parser()
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": "Weather information " "updated.",
            }
        )
