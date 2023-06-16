from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from weather_parser import run_parser
from .models import Weather, ParserTimeSettings
from .serializers import WeatherSerializer, ParserTimeSettingsSerializer


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
    """ It is used to trigger the execution of the run_parser function,
    which updates the weather information."""
    def post(self, request, format=None):
        run_parser()
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": "Weather information " "updated.",
            }
        )


class ParserTimeSettingsView(generics.CreateAPIView):
    """ It is used to update the time when the parser should be run."""
    queryset = ParserTimeSettings.objects.all()
    serializer_class = ParserTimeSettingsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Run the parser with the new time
        run_parser()
        return Response(serializer.data, status=status.HTTP_200_OK)
