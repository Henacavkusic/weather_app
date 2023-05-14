from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse
from datetime import date, datetime
import logging
import requests
import env
from weather_api.models import WeatherData

api_logger = logging.getLogger(__name__)


def current_weather(request):
    location = request.GET['location']
    weather_app_response = cache.get(f"{location}:current", [])
    if not weather_app_response:
        lat, lon, err = get_lat_lon(location)
        if not err:
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={env.OWM_API_KEY}&units=metric"
            api_logger.info(f"Getting current weather data for {location}")
            response = requests.get(url)
            if response.status_code != 200:
                api_logger.error("error: ", response.json())
                return JsonResponse({"error": f"{response.json()}"}, status=response.status_code)

            data = response.json()
            wd = WeatherData(data['current']).to_dict()
            weather_app_response = {"location": location, "data": wd,
                                    "last_refreshed": datetime.now().strftime("%m-%d-%Y %H:%M:%S")}
            cache.set(key=f"{location}:current", value=weather_app_response, timeout=600)
            api_logger.info(f"Weather data retrieved successfully")
            return JsonResponse(weather_app_response)
        return err
    else:
        api_logger.info(f"Weather data retrieved from cache successfully")
        return JsonResponse(weather_app_response)


def forecast_weather(request):
    location = request.GET['location']
    weather_app_response = cache.get(f"{location}:forecast", [])
    if not weather_app_response:
        lat, lon, err = get_lat_lon(location)
        if not err:
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={env.OWM_API_KEY}&units=metric"
            api_logger.info(f"Getting forecast weather data for {location}")
            response = requests.get(url)
            if response.status_code != 200:
                api_logger.error("error: ", response.json())
                return JsonResponse({"error": f"{response.json()}"}, status=response.status_code)

            data = response.json()
            wd = []
            for day in data['daily']:
                wd.append(WeatherData(day).to_dict())
            weather_app_response = {"location": location, "data": wd,
                                    "last_refreshed": datetime.now().strftime("%m-%d-%Y %H:%M:%S")}
            cache.set(key=f"{location}:forecast", value=weather_app_response, timeout=600)
            api_logger.info(f"Weather data retrieved successfully")
            return JsonResponse(weather_app_response)
        return err
    else:
        api_logger.info(f"Weather data retrieved from cache successfully")
        return JsonResponse(weather_app_response)


def history_weather(request):
    location = request.GET['location']
    dt = int(datetime.fromisoformat(request.GET['date']).timestamp())
    weather_app_response = cache.get(f"{location}:history", [])
    if not weather_app_response:
        lat, lon, err = get_lat_lon(location)
        if not err:
            url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&appid={env.OWM_API_KEY}&units=metric"
            api_logger.info(f"Getting weather data for {location} for {request.GET['date']}")
            response = requests.get(url)
            if response.status_code != 200:
                api_logger.error("error: ", response.json())
                return JsonResponse({"error": f"{response.json()}"}, status=response.status_code)

            data = response.json()
            wd = WeatherData(data['data'][0]).to_dict()
            weather_app_response = {"location": location, "data": wd,
                                    "last_refreshed": datetime.now().strftime("%m-%d-%Y %H:%M:%S")}
            cache.set(key=f"{location}:history", value=weather_app_response, timeout=600)
            api_logger.info(f"Weather data retrieved successfully")
            return JsonResponse(weather_app_response)
        return err
    else:
        api_logger.info(f"Weather data retrieved from cache successfully")
        return JsonResponse(weather_app_response)


def get_lat_lon(location):
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&appid={env.OWM_API_KEY}"
    api_logger.info(f"Getting latitude and longitude coordinates for {location}")
    response = requests.get(url)
    if response.status_code != 200:
        api_logger.error("error: ", response.json())
        return 0, 0, JsonResponse({"error": f"{response.json()}"}, status=response.status_code)

    data = response.json()
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon, ''
    return 0, 0, JsonResponse({"error": f"Your location {location} does not exist"}, status=400)

