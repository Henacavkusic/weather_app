from django.shortcuts import render
from django.http import JsonResponse
from datetime import date, datetime
import requests
import env


def current_weather(request):
    location = request.GET['location']
    lat, lon, err = get_lat_lon(location)
    if not err:
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={env.OWM_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code != 200:
            return JsonResponse({"error": f"{response.json()}"}, status=response.status_code)

        data = response.json()
        return JsonResponse({location: make_response(data['current'])})
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
            data_to_return.append(make_response(day))
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
        return JsonResponse({location: make_response(data['data'][0])})
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
    r = {
        "day": date.fromtimestamp(data['dt']).isoformat(),
        "temperature": data['temp'],
        "pressure": data['pressure'],
        "humidity": data['humidity'],
        "wind_speed": data['wind_speed'],
        "clouds": data['clouds'],
        "rain": 0,
        "snow": 0
    }

    if "rain" in data:
        r['rain'] = data['rain']
    if "snow" in data:
        r['snow'] = data['snow']
    if "uvi" in data:
        r['uvi'] = data['uvi']

    return r
