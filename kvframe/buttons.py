from kivy.utils import get_color_from_hex
from kivy.uix.button import Button
from kivy.vector import Vector


class RoundedButton(Button):
    DISABLED_COLOR = get_color_from_hex("#9e9ea2")
    FONT_COLOR = get_color_from_hex("#ffffff")

    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2


class RedButton(RoundedButton):
    UNPRESSED_COLOR = get_color_from_hex("#ff000d")
    PRESSED_COLOR = get_color_from_hex("#be0119")


class GreenButton(RoundedButton):
    UNPRESSED_COLOR = get_color_from_hex("#21fc0d")
    PRESSED_COLOR = get_color_from_hex("#048243")
    FONT_COLOR = get_color_from_hex("#000000")