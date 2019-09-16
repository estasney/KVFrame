import sys
import os

import requests

sys.path.append(os.getcwd())
import threading
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.properties import *

from kvweatherdash.custom import *
from kvweatherdash.utils import ForecastWeather, CurrentWeather


class WeatherDash(App):
    APP_NAME = 'Weather Dash'
    # TODO Increase update frequency when NWS returns "NA"

    screen_manager = ObjectProperty()
    current_data_provider = CurrentWeather
    forecast_data_provider = ForecastWeather
    session = None
    current_weather = DictProperty(rebind=True)
    forecast_weather = ListProperty(rebind=True)
    clock_time = StringProperty()
    forecast_times = DictProperty(rebind=True)
    last_update_time = StringProperty()

    def run_threaded(self, target_function, *args, **kwargs):
        threading.Thread(target=target_function, args=args, kwargs=kwargs).start()

    def _update_property(self, property_name, value):
        setattr(self, property_name, value)

    def _update_current_data(self, *args, **kwargs):
        current_weather = self.current_data_provider.fetch(self.session)
        self._update_property('current_weather', current_weather)
        print(current_weather)

    def update_current_data(self, *args, **kwargs):
        self.run_threaded(self._update_current_data)

    def _update_forecast_data(self, *args, **kwargs):
        forecast_weather = self.forecast_data_provider.fetch(self.session)
        forecast_weather_formatted = self.make_forecast_times(forecast_weather)
        self._update_property('forecast_weather', forecast_weather_formatted)
        print(forecast_weather_formatted)
        self._update_property('last_update_time', self.clock_time)

    def _setup_session(self):
        session = requests.session()
        session.headers.update({
                                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
                                   })
        self.session = session

    def update_forecast_data(self, *args, **kwargs):
        self.run_threaded(self._update_forecast_data)

    def get_time(self, *args, **kwargs):
        self.clock_time = datetime.strftime(datetime.now(), "%I:%M:%S %p")

    def make_forecast_times(self, data, *args, **kwargs):
        # Use current hour as "0-hour".
        output = []
        now = datetime.now()
        hour_zero = datetime(now.year, now.month, now.day, now.hour)
        for dt_k, v in data.items():
            output_k = hour_zero + dt_k
            v['display_time'] = datetime.strftime(output_k, "%a %I:%M %p")
            output.append(v)
        return output

    def build(self):
        self._setup_session()
        self.get_time()
        self._update_current_data()
        self._update_forecast_data()
        sm = WeatherScreen()
        self.screen_manager = sm
        self.screen_manager.create_forecast(self, 2, 10)
        Clock.schedule_interval(self.get_time, 0.1)
        Clock.schedule_interval(self.update_current_data, 900)
        Clock.schedule_interval(self.update_forecast_data, 900)
        return sm


if __name__ == '__main__':
    WeatherDash().run()
