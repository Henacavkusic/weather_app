from django.shortcuts import render
from django.http import JsonResponse
import requests
from weather_app import .env

def current_weather(request, location):
    api_key = "YOUR_API_KEY" # replace with your own API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code != 200:
        return JsonResponse({"error": "Invalid location input"}, status=400)

    data = response.json()
    return JsonResponse(data)


def forecast_weather(request, location):
    pass


def history_weather(request, location, datetime):
    pass
