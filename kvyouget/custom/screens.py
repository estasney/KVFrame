from kivy.clock import mainthread
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from dl.utils import Result
from utils import import_kv

import_kv(__file__)


class KVGScreenManager(ScreenManager):
    app = ObjectProperty()

    def __init__(self, app, **kwargs):
        self.app = app

        super().__init__(**kwargs)

    def handle_itag_result(self, result: Result, *args, **kwargs):
        self.ids['chooser_screen'].set_result(result)
        self.current = 'chooser_screen'


class InputUrlScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LoaderScreen(Screen):

    pass


class ChooserScreen(Screen):
    itags = ListProperty(rebind=True)
    url_title = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_result(self, result: Result, *args, **kwargs):
        print(f"Chooser Screen got Result")
        self.itags = result.itags
        self.url_title = result.title
