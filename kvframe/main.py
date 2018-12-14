from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
import os

class FrameApp(App):
    def __init__(self):
        super().__init__()
        self.icon_path = os.path.realpath("resources/images/logo.png")


if __name__ == "__main__":
    FrameApp().run()
