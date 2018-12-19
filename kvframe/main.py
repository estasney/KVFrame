from kivy.app import App
from kivy.config import Config
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from datetime import datetime
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.vector import Vector
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

class RoundedButton(ButtonBehavior, Label, Widget):
    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2

class WelcomeButton(RoundedButton):
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
