import requests
# url = "https://forecast.weather.gov/MapClick.php?lat=35.643&lon=-78.6043&unit=0&lg=english&FcstType=dwml"
# r = requests.get(url)
import xml.etree.ElementTree as ET
from abc import ABC
root = ET.fromstring(r.content)

forecast = root.find(".//data[@type='forecast']")
current = root.find(".//data[@type='current observations']")


class Selector(object):

    def __init__(self, name, child_path = "/", **kwargs):
        self.name = name
        self.attributes = self.parse_kwargs(kwargs)
        self.child_path = child_path



    def parse_kwargs(self, kwargs):
        kw = {}
        for k, v in kwargs.items():
            if "type" in k:
                kw["type"] = v
            else:
                kw[k] = v
        return kw

    def to_tuple(self):
        base_kw = {'child_path': self.child_path}
        base_kw.update(self.attributes)
        return self.name, base_kw

class MyXMLParser(ABC):

    def helper(self, *args):
        search_str = ""
        for e in args:
            el, attrib = e.to_tuple()
            search_str += el
            child_path = attrib.pop('child_path', None)
            if attrib:
                search_str += "["
                for i, (k, v) in enumerate(attrib.items()):
                    search_str += "@{}='{}'".format(k, v)
                    if (i + 1) == len(attrib):
                        search_str += "]"
                    else:
                        search_str += " and "
            if child_path:
                search_str += child_path

        return search_str



    def parse_tree(self, *args):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError




class ForecastWeatherParser(MyXMLParser):

    def __init__(self):


class CurrentWeatherParser(MyXMLParser):

    PARAMS_ACCESSOR = Selector("parameters")
    TEMPERATURE_APPARENT = Selector("temperature", type="apparent")
    TEMPERATURE_DEW_POINT = Selector("temperature", type="dew point")
    HUMIDITY_RELATIVE = Selector("humidity", type="relative")
    WIND_DIRECTION = Selector("direction", type="wind")
    WIND_SPEED_GUST = Selector("wind-speed", type="gust")
    WIND_SPEED_SUSTAINED = Selector("wind-speed", type="sustained")
    PRESSURE = Selector("pressure", type="barometer")

    DATA_KEYS = ["temperature", "dew_point", "humidity_relative", "weather_summary", "wind_direction", "wind_speed_gust",
                 "wind_speed_sustained", "barometer"]



    def __init__(self, root):
        self.current_element = root.find(".//data[@type='current observations']")
        self.temperature = self.parse_tree(self.PARAMS_ACCESSOR, self.TEMPERATURE_APPARENT)
        self.dew_point = self.parse_tree(self.PARAMS_ACCESSOR, self.TEMPERATURE_DEW_POINT)
        self.humidity_relative = self.parse_tree(self.PARAMS_ACCESSOR, self.HUMIDITY_RELATIVE)
        self.weather_summary = self.current_element.find(".//weather-conditions").attrib.get('weather-summary', None)
        self.wind_direction = self.parse_tree(self.PARAMS_ACCESSOR, self.WIND_DIRECTION)
        self.wind_speed_gust = self.parse_tree(self.PARAMS_ACCESSOR, self.WIND_SPEED_GUST)
        self.wind_speed_sustained = self.parse_tree(self.PARAMS_ACCESSOR, self.WIND_SPEED_SUSTAINED)
        self.barometer = self.parse_tree(self.PARAMS_ACCESSOR, self.PRESSURE)


    def parse_tree(self, *args):
        search_str = self.helper(*args)
        found = self.current_element.find(search_str).text
        return found

    def to_dict(self):
        data_out = {}
        for k in self.DATA_KEYS:
            data_out[k] = getattr(self, k)
        return data_out