from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
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

class DownloadButtonBar(BoxLayout):

    input_element = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
