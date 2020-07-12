import sys
import os

import requests
from dotenv import load_dotenv
import threading
from datetime import datetime

from kivy.clock import Clock
from kivy.properties import *

from kvweatherdash.custom import *
from kvweatherdash.utils import ForecastWeather, CurrentWeather, SunProvider


class WeatherDash(App):
    APP_NAME = 'Weather Dash'
    # TODO Increase update frequency when NWS returns "NA"

    screen_manager = ObjectProperty()
    current_data_provider = CurrentWeather
    forecast_data_provider = ForecastWeather
    sun_data_provider = SunProvider
    session = None
    current_weather = DictProperty(rebind=True)
    forecast_weather_hourly = ListProperty(rebind=True)
    forecast_weather_daily = DictProperty(rebind=True)
    clock_time = StringProperty()
    forecast_times = DictProperty(rebind=True)
    last_update_time = StringProperty()
    sunrise_time = StringProperty()
    sunset_time = StringProperty()
    weather_longitude = None
    weather_latitude = None
    sun_longitude = None
    sun_latitude = None

    def run_threaded(self, target_function, *args, **kwargs):
        threading.Thread(target=target_function, args=args, kwargs=kwargs).start()

    def _update_property(self, property_name, value):
        setattr(self, property_name, value)

    def _update_sun_data(self, *args, **kwargs):
        sun_data = self.sun_data_provider.fetch(latitude=self.sun_latitude,
                                                longitude=self.sun_longitude, session=self.session)['results']
        sunrise = datetime.fromisoformat(sun_data['sunrise']).astimezone()
        sunset = datetime.fromisoformat(sun_data['sunset']).astimezone()

        sunrise_str = datetime.strftime(sunrise, "%I:%M %p")
        sunset_str = datetime.strftime(sunset, "%I:%M %p")
        self._update_property('sunrise_time', sunrise_str)
        self._update_property('sunset_time', sunset_str)

    def update_sun_data(self, *args, **kwargs):
        self.run_threaded(self._update_sun_data)

    def _update_current_data(self, *args, **kwargs):
        current_weather = self.current_data_provider.fetch(latitude=self.weather_latitude,
                                                           longitude=self.weather_longitude, session=self.session)
        self._update_property('current_weather', current_weather)
        print(current_weather)

    def update_current_data(self, *args, **kwargs):
        self.run_threaded(self._update_current_data)

    def _update_forecast_data(self, *args, **kwargs):
        forecast_weather = self.forecast_data_provider.fetch(latitude=self.weather_latitude,
                                                             longitude=self.weather_longitude,
                                                             session=self.session)
        forecast_weather_formatted = self.make_forecast_times(forecast_weather)
        self._update_property('forecast_weather_hourly', forecast_weather_formatted)
        print(forecast_weather_formatted)
        forecast_weather_daily = self.forecast_data_provider.daily_high_lows(forecast_weather)
        self._update_property('forecast_weather_daily', forecast_weather_daily)
        self._update_property('last_update_time', self.clock_time)

    def _setup_session(self):
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 '
                          'Safari/537.36 '
            })
        self.session = session

    def update_forecast_data(self, *args, **kwargs):
        self.run_threaded(self._update_forecast_data)

    def get_time(self, *args, **kwargs):
        self.clock_time = datetime.strftime(datetime.now(), "%I:%M %p")

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
        try:
            self.weather_latitude = float(os.getenv("WEATHER_LATITUDE"))
            self.weather_longitude = float(os.getenv("WEATHER_LONGITUDE"))
        except ValueError:
            raise EnvironmentError(r"Requires WEATHER_LATITUDE and WEATHER_LONGITUDE in .env file")
        self.sun_latitude = os.getenv("SUN_LATITUDE", self.weather_latitude)
        self.sun_longitude = os.getenv("SUN_LONGITUDE", self.weather_longitude)
        self._setup_session()
        self.get_time()
        self._update_current_data()
        self._update_forecast_data()
        self._update_sun_data()
        sm = WeatherScreen()
        self.screen_manager = sm
        self.screen_manager.create_hourly_forecast(app=self, hour_interval=1, max_rows=8)
        self.screen_manager.create_daily_forecast(app=self, n_days=3)
        Clock.schedule_interval(self.get_time, 10)
        Clock.schedule_interval(self.update_current_data, 900)
        Clock.schedule_interval(self.update_forecast_data, 900)
        Clock.schedule_interval(self.update_sun_data, 43200)
        return sm


if __name__ == '__main__':
    sys.path.append(os.getcwd())
    load_dotenv()
    WeatherDash().run()
