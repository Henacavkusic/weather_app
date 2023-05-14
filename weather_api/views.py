from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from datetime import datetime
import logging
import requests

from env import OWM_API_KEY
from weather_api.models import WeatherData

api_logger = logging.getLogger(__name__)


@api_view(['POST'])
def create_user(request):
    print(request)
    # Extract the username and password from the request data
    username = request.data.get('username')
    password = request.data.get('password')

    # Check if the username and password were provided
    if not username or not password:
        return JsonResponse({"error": "Please provide both username and password"}, status=400)

    # Check if the username is already taken
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username is already taken"}, status=400)

    # Create the user and set their password
    user = User.objects.create_user(username=username, password=password)
    return JsonResponse({"success": f"User: {user.username} created successfully"}, status=201)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def current_weather(request):
    print(request)
    # Extract the location from the request query params
    location = request.GET['location']
    # Getting cached response from redis if not expired
    weather_app_response = cache.get(f"{location}:current", [])
    if not weather_app_response:
        # Getting latitude and longitude for requested location
        lat, lon, err = get_lat_lon(location)
        if not err:
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={OWM_API_KEY}&units=metric"
            api_logger.info(f"Getting current weather data for {location}")
            response = requests.get(url)
            if response.status_code != 200:
                api_logger.error("error: ", response.json())
                return JsonResponse({"error": f"{response.json()}"}, status=response.status_code)

            data = response.json()
            wd = WeatherData(data['current']).to_dict()
            # Creating final response
            weather_app_response = {"location": location, "data": wd,
                                    "last_refreshed": datetime.now().strftime("%m-%d-%Y %H:%M:%S")}
            cache.set(key=f"{location}:current", value=weather_app_response, timeout=600)
            # Caching response for 10 min in redis
            api_logger.info(f"Weather data retrieved successfully")
            return JsonResponse({"success": weather_app_response}, status=200)
        return err
    else:
        api_logger.info(f"Weather data retrieved from cache successfully")
        return JsonResponse({"success": weather_app_response}, status=200)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def forecast_weather(request):
    # Extract the location from the request query params
    location = request.GET['location']
    # Getting cached response from redis if not expired
    weather_app_response = cache.get(f"{location}:forecast", [])
    if not weather_app_response:
        # Getting latitude and longitude for requested location
        lat, lon, err = get_lat_lon(location)
        if not err:
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={OWM_API_KEY}&units=metric"
            api_logger.info(f"Getting forecast weather data for {location}")
            response = requests.get(url)
            if response.status_code != 200:
                api_logger.error("error: ", response.json())
                return JsonResponse({"error": f"{response.json()}"}, status=response.status_code)

            data = response.json()
            wd = []
            for day in data['daily']:
                wd.append(WeatherData(day).to_dict())
            # Creating final response
            weather_app_response = {"location": location, "data": wd,
                                    "last_refreshed": datetime.now().strftime("%m-%d-%Y %H:%M:%S")}
            cache.set(key=f"{location}:forecast", value=weather_app_response, timeout=600)
            # Caching response for 10 min in redis
            api_logger.info(f"Weather data retrieved successfully")
            return JsonResponse({"success": weather_app_response}, status=200)
        return err
    else:
        api_logger.info(f"Weather data retrieved from cache successfully")
        return JsonResponse({"success": weather_app_response}, status=200)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def history_weather(request):
    # Extract the location and date from the request query params
    location = request.GET['location']
    dt = int(datetime.fromisoformat(request.GET['date']).timestamp())
    # Getting cached response from redis if not expired
    weather_app_response = cache.get(f"{location}:history", [])
    if not weather_app_response:
        # Getting latitude and longitude for requested location
        lat, lon, err = get_lat_lon(location)
        if not err:
            url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&appid={OWM_API_KEY}&units=metric"
            api_logger.info(f"Getting weather data for {location} for {request.GET['date']}")
            response = requests.get(url)
            if response.status_code != 200:
                api_logger.error("error: ", response.json())
                return JsonResponse({"error": f"{response.json()}"}, status=response.status_code)

            data = response.json()
            wd = WeatherData(data['data'][0]).to_dict()
            # Creating final response
            weather_app_response = {"location": location, "data": wd,
                                    "last_refreshed": datetime.now().strftime("%m-%d-%Y %H:%M:%S")}
            # Caching response for 10 min in redis
            cache.set(key=f"{location}:history", value=weather_app_response, timeout=600)
            api_logger.info(f"Weather data retrieved successfully")
            return JsonResponse({"success": weather_app_response}, status=200)
        return err
    else:
        api_logger.info(f"Weather data retrieved from cache successfully")
        return JsonResponse({"success": weather_app_response}, status=200)


def get_lat_lon(location):
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&appid={OWM_API_KEY}"
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