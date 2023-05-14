from django.shortcuts import render
from django.http import JsonResponse
from datetime import date, datetime
import requests
import env
from weather_api.models import WeatherData


def current_weather(request):
    location = request.GET['location']
    lat, lon, err = get_lat_lon(location)
    if not err:
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={env.OWM_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code != 200:
            return JsonResponse({"error": f"{response.json()}"}, status=response.status_code)

        data = response.json()
        return JsonResponse({location: WeatherData(data['current']).to_dict()})
    return err


def forecast_weather(request):
    location = request.GET['location']
    lat, lon, err = get_lat_lon(location)
    if not err:
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={env.OWM_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code != 200:
            return JsonResponse({"error": f"{response.json()}"}, status=response.status_code)

        data = response.json()
        data_to_return = []
        for day in data['daily']:
            data_to_return.append(WeatherData(day).to_dict())
        return JsonResponse({location: data_to_return})
    return err


def history_weather(request):
    location = request.GET['location']
    dt = int(datetime.fromisoformat(request.GET['date']).timestamp())
    lat, lon, err = get_lat_lon(location)
    if not err:
        url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&appid={env.OWM_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code != 200:
            return JsonResponse({"error": f"{response.json()}"}, status=response.status_code)

        data = response.json()
        return JsonResponse({location: WeatherData(data['data'][0]).to_dict()})
    return err


def get_lat_lon(location):
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&appid={env.OWM_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return 0, 0, JsonResponse({"error": f"{response.json()}"}, status=response.status_code)

    data = response.json()
    lat = data[0]['lat']
    lon = data[0]['lon']
    return lat, lon, ''


def make_response(data):
    return
