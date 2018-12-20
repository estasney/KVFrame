from kivy.app import App
from kivy.config import Config
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from datetime import datetime
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.vector import Vector
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')


class MainScreen(Screen):
    pass

class ScreenNav(FloatLayout):
    pass

class SplashScreen(Screen):
    icon_path = os.path.realpath("resources/images/logo.png")

class ScreenManagement(ScreenManager):
    pass

class StatusBar(BoxLayout):
    pass

class StatusComponent(BoxLayout):
    pass

class RoundedButton(ButtonBehavior, Label):
    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2

class ButtonGreen(AnchorLayout):
    def get_up(self):
        return os.path.realpath("resources/images/light_green.png")
    def get_down(self):
        return os.path.realpath("resources/images/dark_green.png")

class WelcomeButton(RoundedButton):
    pass



class MainApp(App):

    clock_time = StringProperty()
    resource_dir = StringProperty()

    def get_time(self, *args, **kwargs):
        self.clock_time = datetime.strftime(datetime.now(), "%I:%M:%S %p")

    def build(self):
        self.get_time()
        Clock.schedule_interval(self.get_time, 0.1)



if __name__ == "__main__":

    MainApp().run()
