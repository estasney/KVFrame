from kivy.app import App
from kivy.config import Config
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from datetime import datetime
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')


class MainScreen(Screen):
    pass

class SplashScreen(Screen):
    icon_path = os.path.realpath("resources/images/logo.png")

class ScreenManagement(ScreenManager):
    pass

class Holder(BoxLayout):
    pass


class MainApp(App):

    clock_time = StringProperty()

    def get_time(self, *args, **kwargs):
        self.clock_time = datetime.strftime(datetime.now(), "%I:%M:%S %p")

    def build(self):
        self.get_time()
        Clock.schedule_interval(self.get_time, 0.1)



if __name__ == "__main__":

    MainApp().run()
