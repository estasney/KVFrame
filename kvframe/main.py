from kivy.app import App
from kivy.config import Config
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')


class MainScreen(Screen):
    pass

class SplashScreen(Screen):
    icon_path = os.path.realpath("resources/images/logo.png")

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return presentation

if __name__ == "__main__":
    MainApp().run()
