import os

from kivy.app import App
from kivy.properties import StringProperty, DictProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivy.vector import Vector

from utils import import_kv

import_kv(__file__)


class RoundedButton(Button):
    DISABLED_COLOR = get_color_from_hex("#9e9ea2")
    FONT_COLOR = get_color_from_hex("#ffffff")

    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2


class RedButton(RoundedButton):
    UNPRESSED_COLOR = StringProperty(get_color_from_hex("#ff000d"))
    PRESSED_COLOR = StringProperty(get_color_from_hex("#be0119"))


class GreenButton(RoundedButton):
    UNPRESSED_COLOR = StringProperty(get_color_from_hex("#21fc0d"))
    PRESSED_COLOR = StringProperty(get_color_from_hex("#048243"))
    FONT_COLOR = StringProperty(get_color_from_hex("#000000"))


class ImageButton(ButtonBehavior, Image):

    def __init__(self, src, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = src

    def collide_point(self, x, y):
        distance = Vector(x, y).distance(self.center)
        return distance <= self.norm_image_size[0] / 2


class DynamicImageButton(ButtonBehavior, Image):
    sources = DictProperty()
    current_source = StringProperty()

    def __init__(self, current_source: str, sources: dict, *args, **kwargs):
        self.sources = sources
        self.current_source = current_source
        self.source = self.sources[self.current_source]
        super().__init__()

    def collide_point(self, x, y):
        distance = Vector(x, y).distance(self.center)
        return distance <= self.norm_image_size[0] / 2


class PlayStateButton(DynamicImageButton):
    sources = DictProperty()
    current_source = StringProperty()
    app = ObjectProperty()

    def __init__(self, *args, **kwargs):
        self.app = App.get_running_app()
        self.app.bind(play_state=self.setter('current_source'))
        super().__init__(current_source="play",
                         sources={
                             "play":  "atlas://static/icons/button_bar/play",
                             "pause": "atlas://static/icons/button_bar/pause"
                             })

    def on_current_source(self, old, new):
        self.source = self.sources[new]


class BackButton(ImageButton):

    def __init__(self, *args, **kwargs):
        super().__init__(src="atlas://static/icons/button_bar/back")


class ForwardButton(ImageButton):

    def __init__(self, *args, **kwargs):
        super().__init__(src="atlas://static/icons/button_bar/forward")


class ReturnButton(ImageButton):

    def __init__(self, *args, **kwargs):
        super().__init__(src="atlas://static/icons/button_bar/back_arrow")

class ListViewButton(ImageButton):

    def __init__(self, *args, **kwargs):
        super().__init__(src="atlas://static/icons/button_bar/list_view")
