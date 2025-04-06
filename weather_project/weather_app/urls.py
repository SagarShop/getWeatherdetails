from django.urls import path
from .views import GetCurrentWeather

urlpatterns = [
    path("getCurrentWeather", GetCurrentWeather.as_view(), name="get_weather"),
]
