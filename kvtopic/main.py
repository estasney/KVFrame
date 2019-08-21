from kivy.app import App
from kivy.config import Config
import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, ListProperty, NumericProperty, DictProperty
from kivy.clock import Clock
from datetime import datetime
from buttons import RedButton, GreenButton, RoundedButton

import threading

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')



class ScreenManagement(ScreenManager):
    pass


class SplashScreen(Screen):
    pass


class TopicApp(App):
    APP_NAME = "KVTopic"
    APP_VERSION_ = 1
    APP_VERSION = "v{}".format(APP_VERSION_)
    APP_ICON_PATH = os.path.realpath("resources/logo.png")
    GREEN_TEXT = "#21fc0d"
    RED_TEXT = "#fe420f"

    clock_time = StringProperty()
    resource_dir = StringProperty()

    def get_time(self, *args, **kwargs):
        self.clock_time = datetime.strftime(datetime.now(), "%I:%M:%S %p")

    def build(self):
        self.get_time()
        Clock.schedule_interval(self.get_time, 0.1)


if __name__ == "__main__":
    TopicApp().run()
