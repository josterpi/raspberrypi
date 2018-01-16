
import json
import urllib.request

from .secrets import WEATHER_KEY, CITY_ID

API = "http://api.openweathermap.org/data/2.5/weather?units=imperial&id=%s&appid=%s"

def get_url():
    return API % (CITY_ID, WEATHER_KEY)

def get_weather():
    res = urllib.request.urlopen(get_url())
    weather = json.loads(res.read().decode('utf-8'))
    return weather
