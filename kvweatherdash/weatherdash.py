from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import *

from kvweatherdash.custom import *


class WeatherDash(App):
    APP_NAME = 'Weather Dash'

    screen_manager = ObjectProperty()
    api_key = None
    network_manager = None
    clock_time = StringProperty()

    def get_time(self, *args, **kwargs):
        self.clock_time = datetime.strftime(datetime.now(), "%I:%M:%S %p")

    def get_api_key(self):
        with open(r"kvweatherdash/resources/api_key.txt", "rb") as fp:
            self.api_key = fp.read().strip()

    def build(self):
        self.get_time()
        sm = WeatherScreen()
        self.screen_manager = sm
        Clock.schedule_interval(self.get_time, 0.1)
        return sm

if __name__ == '__main__':
    WeatherDash().run()