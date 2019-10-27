from abc import ABC
import xml.etree.ElementTree as ET
from datetime import datetime
from functools import partial
from itertools import zip_longest

import pandas as pd
import requests


class Selector(object):

    def __init__(self, name, child_path="/", **kwargs):
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
    URL = ""

    def helper(self, *args, trailing_slash=True):
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
        if search_str[-1] == "/" and trailing_slash is False:
            return search_str[:-1]
        return search_str


class ForecastWeather(MyXMLParser):
    URL = "https://forecast.weather.gov/MapClick.php?lat=35.643&lon=-78.6043&FcstType=digitalDWML"
    DATA_NODE = Selector("data")
    PARAMS_ACCESSOR = Selector("parameters")
    TIME_LAYOUTS = Selector("time-layout")
    TEMPERATURE_HOURLY = Selector("temperature", type="hourly", child_path="")
    TEMPERATURE_HEAT_INDEX = Selector("temperature", type="heat index", child_path="")
    TEMPERATURE_DEW_POINT = Selector("temperature", type="dew point", child_path="")
    WINDSPEED = Selector("wind-speed", type="sustained", child_path="")
    CLOUDS = Selector("cloud-amount", type="total", child_path="")
    HUMIDITY = Selector("humidity", type="relative", child_path="")

    PRECIPITATION_PROBABILITY = Selector("probability-of-precipitation", type='floating', child_path="")
    PRECIPITATION_QPF = Selector("hourly-qpf", type="floating", child_path="")

    DATA_KEYS = ["temperature_hourly", "temperature_heat_index", "clouds", "humidity", "precipitation_probability",
                 "precipitation_qpf"]

    def __init__(self, xml: str):
        self.root = ET.fromstring(xml)
        self.params = self.root.find(self.helper(self.DATA_NODE, self.PARAMS_ACCESSOR, trailing_slash=False))
        self._temperature_hourly = self.params.find(self.helper(self.TEMPERATURE_HOURLY, trailing_slash=False))
        self._temperature_heat_index = self.params.find(self.helper(self.TEMPERATURE_HEAT_INDEX, trailing_slash=False))
        self._clouds = self.params.find(self.helper(self.CLOUDS, trailing_slash=False))
        self._humidity = self.params.find(self.helper(self.HUMIDITY, trailing_slash=False))
        self._probability_of_precipitation = self.params.find(
                self.helper(self.PRECIPITATION_PROBABILITY, trailing_slash=False))
        self._precipitation_qpf = self.params.find(self.helper(self.PRECIPITATION_QPF, trailing_slash=False))
        self.time_layout_node = self.root.find(self.helper(self.DATA_NODE, self.TIME_LAYOUTS, trailing_slash=False))
        self.time_layout = self._time_layout()
        self.time_offsets = self._time_offsets()

    def strip_utc_offset(self, x):
        s = x.replace("-04:00", "")
        return s

    def _time_layout(self):
        seen = set([])
        output = []
        for x in self.time_layout_node[1:]:
            xtext = self.strip_utc_offset(x.text)
            if xtext in seen:
                continue
            output.append(xtext)
            seen.add(xtext)
        return output

    def _time_offsets(self):
        times = sorted([datetime.fromisoformat(x) for x in self.time_layout])
        time_delta = [(x - times[0]) for x in times[1:]]
        return time_delta

    def _to_int(self, x):
        try:
            return int(x)
        except TypeError:
            return 0

    def _to_float(self, x, convert_pct=False):
        try:
            x = float(x)
            if convert_pct:
                x /= 100
            return float(x)
        except TypeError:
            return 0

    def _get_values(self, attr, as_type=None, **kwargs):
        if not as_type:
            f = lambda x: x
        elif as_type == int:
            f = self._to_int
        elif as_type == float:
            convert_pct = kwargs.get('convert_pct', False)
            f = partial(self._to_float, convert_pct=convert_pct)

        else:
            f = lambda x: x
        attr_val = getattr(self, attr)
        if attr_val is None:
            return []
        else:
            return [f(x.text) for x in attr_val[1:]]


    @property
    def temperature_hourly(self):
        return self._get_values('_temperature_hourly', as_type=int)

    @property
    def temperature_heat_index(self):
        return self._get_values("_temperature_heat_index", as_type=int)

    @property
    def clouds(self):
        return self._get_values("_clouds", as_type=float)

    @property
    def humidity(self):
        return self._get_values("_humidity", as_type=float)

    @property
    def precipitation_probability(self):
        return self._get_values("_probability_of_precipitation", as_type=float)

    @property
    def precipitation_qpf(self):
        return self._get_values("_precipitation_qpf", as_type=float)

    def to_dict(self):
        data_out = {}
        # create an zipped iterator
        data_iter = zip_longest(*[getattr(self, k) for k in self.DATA_KEYS])
        for td in self.time_offsets:
            try:
                td_data = next(data_iter)
            except StopIteration:
                break
            td_dict = {}
            for i, k in enumerate(self.DATA_KEYS):
                td_dict[k] = td_data[i]
            data_out[td] = td_dict
        return data_out

    @classmethod
    def fetch(cls, session: requests.session):
        r = session.get(cls.URL).content
        forecast = cls(r)
        return forecast.to_dict()


class CurrentWeather(MyXMLParser):
    URL = "https://forecast.weather.gov/MapClick.php?lat=35.643&lon=-78.6043&unit=0&lg=english&FcstType=dwml"
    PARAMS_ACCESSOR = Selector("parameters")
    TEMPERATURE_APPARENT = Selector("temperature", type="apparent")
    TEMPERATURE_DEW_POINT = Selector("temperature", type="dew point")
    HUMIDITY = Selector("humidity", type="relative")
    WIND_DIRECTION = Selector("direction", type="wind")
    WIND_SPEED_GUST = Selector("wind-speed", type="gust")
    WIND_SPEED_SUSTAINED = Selector("wind-speed", type="sustained")
    PRESSURE = Selector("pressure", type="barometer")

    DATA_KEYS = ["temperature", "dew_point", "humidity", "weather_summary", "wind_direction",
                 "wind_speed_gust",
                 "wind_speed_sustained", "barometer"]

    def __init__(self, xml: str):
        self.root = ET.fromstring(xml)
        self.current_element = self.root.find(".//data[@type='current observations']")
        self.temperature = self.parse_tree(self.PARAMS_ACCESSOR, self.TEMPERATURE_APPARENT)
        self.dew_point = self.parse_tree(self.PARAMS_ACCESSOR, self.TEMPERATURE_DEW_POINT)
        self.humidity = self.parse_tree(self.PARAMS_ACCESSOR, self.HUMIDITY)
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

    @classmethod
    def fetch(cls, session: requests.session):
        r = session.get(cls.URL).content
        forecast = cls(r)
        return forecast.to_dict()

class SunProvider(object):

    URL = 'http://api.sunrise-sunset.org/json?lat=35.643370&lng=-78.604248&formatted=0'

    def __init__(self):
        pass

    @classmethod
    def fetch(cls, session: requests.session):
        r = session.get(cls.URL).json()
        return r