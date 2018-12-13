from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '1186')
Config.set('graphics', 'height', '567')

class FrameApp(App):
    pass

if __name__ == "__main__":
    FrameApp().run()
