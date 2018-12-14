from kivy.app import App
from kivy.config import Config
import os
from kivy.uix.boxlayout import BoxLayout
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')


class SplashScreen(BoxLayout):

    icon_path = os.path.realpath("resources/images/logo.png")

class FrameApp(App):
    pass


if __name__ == "__main__":
    FrameApp().run()
