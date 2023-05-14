from django.db import models
from datetime import date, datetime


class WeatherData:

    def __init__(self, data_dict: dict):
        self.date: date = date.fromtimestamp(data_dict.get('dt', 0))
        self.temperature: float = data_dict.get('temp', 0.0)
        self.pressure: float = data_dict.get('pressure', 0.0)
        self.humidity: float = data_dict.get('humidity', 0.0)
        self.wind_speed: float = data_dict.get('wind_speed', 0.0)
        self.clouds: float = data_dict.get('clouds', 0.0)
        self.rain: float = data_dict.get('rain', 0.0)
        self.uvi: float = data_dict.get('uvi', 0.0)

    def to_dict(self) -> dict:
        return {
            'date': self.date,
            'temperature': self.temperature,
            'pressure': self.pressure,
            'humidity': self.humidity,
            'wind_speed': self.wind_speed,
            'clouds': self.clouds,
            'rain': self.rain,
            'uvi': self.uvi
        }
