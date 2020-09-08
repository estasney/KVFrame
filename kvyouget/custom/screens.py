from kivy.properties import ObjectProperty, OptionProperty, BooleanProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from utils import import_kv

import_kv(__file__)


class KVGScreenManager(ScreenManager):
    app = ObjectProperty()

    def __init__(self, app, **kwargs):
        self.app = app

        super().__init__(**kwargs)


class InputUrlScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ChooserScreen(Screen):

    is_loaded = BooleanProperty()
    itags = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


