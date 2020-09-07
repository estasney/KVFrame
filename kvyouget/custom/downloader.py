from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from utils import import_kv

import_kv(__file__)


class Downloader(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
