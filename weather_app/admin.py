from django.contrib import admin

from weather_app.models import Weather, ParserTimeSettings

admin.site.register(Weather)
admin.site.register(ParserTimeSettings)
