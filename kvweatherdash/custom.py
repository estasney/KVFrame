from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import Screen, ScreenManager


class CurrentWeather(Screen):
    pass

class Temperature(BoxLayout):
    pass


class WeatherScreen(ScreenManager):
    pass

import requests
url = "https://forecast.weather.gov/MapClick.php?lat=35.643&lon=-78.6043&unit=0&lg=english&FcstType=dwml"
r = requests.get(url)

import xml.etree.ElementTree as ET
root = ET.fromstring(r.content)

forecast = root.find(".//data[@type='forecast']")
current = root.find(".//data[@type='current observations']")


class NetworkManager(object):
    # https: // forecast.weather.gov / MapClick.php?lon = -78.60425949096681 & lat = 35.64299847375348