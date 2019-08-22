from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager




class OptionsScreen(Screen):
    pass

class StatusBar(BoxLayout):
    status_label = ObjectProperty()


class ScreenManagement(ScreenManager):
    pass


class SplashScreen(Screen):
    pass


class DocumentScreen(Screen):
    pass