from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from utils import import_kv

import_kv(__file__)


class Downloader(BoxLayout):
    # url_prefix = StringProperty("https://www.youtube.com/watch?v=FMvppuS_ehg")
    url_prefix = StringProperty("https://www.youtube.com/watch?v=")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
