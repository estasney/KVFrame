from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, DictProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App

from kvweatherdash.weatherdash import WeatherDash


class CurrentWeather(BoxLayout):
    pass

class ForecastWeather(BoxLayout):

    def add_future_weather(self, idx):
        self.add_widget(FutureWeather(idx=idx))

class Weather(Screen):
    current_weather = ObjectProperty()
    forecast_weather = ObjectProperty()

    def add_future_weather(self, idx):
        self.forecast_weather.add_future_weather(idx=idx)


class IntegerProperty(object):
    pass


class FutureWeather(BoxLayout):

    idx = IntegerProperty()

    def __init__(self, **kwargs):
        self.idx = kwargs.pop('idx')
        super().__init__(**kwargs)




class Temperature(BoxLayout):
    pass


class WeatherScreen(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_forecast(self, app:WeatherDash, hour_interval:int, max_rows=5):
        interval_range = range(len(app.forecast_weather))
        row_counter = 0
        for i in interval_range[::hour_interval]:
            if row_counter <= max_rows:
                self.ids['weather'].add_future_weather(i)
                row_counter += 1
            else:
                return



