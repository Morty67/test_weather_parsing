FROM python:3.11.0-slim-buster
LABEL maintainer="gkarabetskii@gmail.com"

ENV PYTHONUNBUFFERED 1
# Installing project dependencies.
COPY requirements.txt /code/
WORKDIR /code
RUN pip install -r requirements.txt

# Copying project source code.
COPY . /code/

# Setting the environment variable DJANGO_SETTINGS_MODULE.
ENV DJANGO_SETTINGS_MODULE=weather_parsing.settings
