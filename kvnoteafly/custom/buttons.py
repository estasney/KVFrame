import os

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivy.uix.button import Button
from kivy.vector import Vector
from kivy.properties import StringProperty


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

    def on_press(self):
        print("pressed")
        return True


class BackButton(ImageButton):

    def __init__(self, *args, **kwargs):
        super(BackButton, self).__init__(src=os.path.join("static", "icons", "back_arrow.png"), *args, **kwargs)
