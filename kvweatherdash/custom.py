from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, DictProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App

from kvweatherdash.weatherdash import WeatherDash


class CurrentWeather(BoxLayout):
    pass


class ForecastWeatherHourly(BoxLayout):

    def add_future_weather(self, idx):
        self.add_widget(FutureWeatherHourly(idx=idx))


class ForecastWeatherDaily(BoxLayout):

    def add_future_weather(self, idx):
        self.add_widget(FutureWeatherDaily(idx=idx))


class WeatherHourly(Screen):
    current_weather = ObjectProperty()
    forecast_weather_hourly = ObjectProperty()

    def add_future_weather(self, idx):
        self.forecast_weather_hourly.add_future_weather(idx=idx)


class WeatherDaily(Screen):
    current_weather = ObjectProperty()
    forecast_weather_daily = ObjectProperty()

    def add_future_weather(self, idx):
        self.forecast_weather_daily.add_future_weather(idx=idx)


class IntegerProperty(object):
    pass


class FutureWeatherHourly(BoxLayout):
    idx = IntegerProperty()

    def __init__(self, **kwargs):
        self.idx = kwargs.pop('idx')
        super().__init__(**kwargs)


class FutureWeatherDaily(BoxLayout):
    idx = IntegerProperty()

    def __init__(self, **kwargs):
        self.idx = kwargs.pop('idx')
        super().__init__(**kwargs)


class Temperature(BoxLayout):
    pass


class WeatherScreen(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        cur = self.current
        self.current = 'weather_hourly' if cur == 'weather_daily' else 'weather_daily'

    def create_hourly_forecast(self, app: WeatherDash, hour_interval: int, max_rows=5):
        interval_range = range(len(app.forecast_weather_hourly))
        row_counter = 0
        for i in interval_range[::hour_interval]:
            if row_counter <= max_rows:
                self.ids['weather_hourly'].add_future_weather(i)
                row_counter += 1
            else:
                return

    def create_daily_forecast(self, app: WeatherDash, n_days: int):
        available_days = list(app.forecast_weather_daily.keys())
        for day in available_days[:n_days]:
            self.ids['weather_daily'].add_future_weather(day)
