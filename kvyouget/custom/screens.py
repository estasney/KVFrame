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
        self.ids['chooser_screen'].set_result(result, *args, **kwargs)
        self.current = 'chooser_screen'


class InputUrlScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LoaderScreen(Screen):

    pass


class ChooserScreen(Screen):
    url_title = StringProperty("")
    child_object = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_result(self, result: Result, *args, **kwargs):
        print(f"Chooser Screen got Result")
        self.url_title = result.title
        self.child_object.set(result)
