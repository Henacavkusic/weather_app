from django.urls import path
from weather_api import views

urlpatterns = [
    path('user/create/', views.create_user, name='create_user'),
    path("weather/current/", views.current_weather, name="current_weather"),
    path("weather/forecast/", views.forecast_weather, name="forecast_weather"),
    path("weather/history/", views.history_weather, name='history_weather'),

]
