from kivy.utils import get_color_from_hex
from kivy.uix.button import Button
from kivy.vector import Vector
from kivy.properties import StringProperty, ListProperty
from colour import Color
from kivy.lang import Builder

Builder.load_file('buttons/buttons.kv')

def pick_font_color(rgb_tuple: tuple, luminance_threshold: float = 0.5) -> tuple:
    """
    Given a background color, determine whether a font should be black or white based on calculated luminance
    :param color_str: Color string such as hex, RGB, etc
    :param luminance_threshold: Luminances above this threshold return 'black', below returns 'white'
    :return: 'black' or 'white'
    """
    c = Color()
    c.rgb = rgb_tuple
    lum = c.get_luminance()
    if lum >= luminance_threshold:
        return [0, 0, 0, 1]
    else:
        return [1, 1, 1, 1]


class ColoredButton(Button):
    UNPRESSED_COLOR = ListProperty(get_color_from_hex("#757575"))
    PRESSED_COLOR = ListProperty(get_color_from_hex("#9e9e9e"))
    FONT_COLOR = ListProperty(get_color_from_hex("#ffffff"))
    DISABLED_COLOR = PRESSED_COLOR

    _FONT_PRESSED_COLOR = None
    _FONT_UNPRESSED_COLOR = None

    def on_state(self, *args, **kwargs):
        if self.state == 'normal':
            if not self._FONT_PRESSED_COLOR:
                self._FONT_PRESSED_COLOR = pick_font_color(tuple(self.UNPRESSED_COLOR[:3]))
            self.FONT_COLOR = self._FONT_PRESSED_COLOR

        else:
            if not self._FONT_UNPRESSED_COLOR:
                self._FONT_UNPRESSED_COLOR = pick_font_color(tuple(self.PRESSED_COLOR[:3]))
            self.FONT_COLOR = self._FONT_UNPRESSED_COLOR


class GrayColoredButton(ColoredButton):
    pass

class RedDarkColoredButton(ColoredButton):
    PRESSED_COLOR = ListProperty(get_color_from_hex("#f9683a"))
    UNPRESSED_COLOR = ListProperty(get_color_from_hex("#bf360c"))
    FONT_COLOR = ListProperty(get_color_from_hex("#ffffff"))

class GreenDarkColoredButton(ColoredButton):
    PRESSED_COLOR = ListProperty(get_color_from_hex("#60ad5e"))
    UNPRESSED_COLOR = ListProperty(get_color_from_hex("#2e7d32"))
    FONT_COLOR = ListProperty(get_color_from_hex("#ffffff"))


class RoundedButton(Button):
    DISABLED_COLOR = get_color_from_hex("#9e9ea2")
    FONT_COLOR = get_color_from_hex("#ffffff")

    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2


class RedRoundedButton(RoundedButton):
    UNPRESSED_COLOR = StringProperty(get_color_from_hex("#ff000d"))
    PRESSED_COLOR = StringProperty(get_color_from_hex("#be0119"))


class GreenRoundedButton(RoundedButton):
    UNPRESSED_COLOR = StringProperty(get_color_from_hex("#21fc0d"))
    PRESSED_COLOR = StringProperty(get_color_from_hex("#048243"))
    FONT_COLOR = StringProperty(get_color_from_hex("#000000"))

class GrayRoundedButton(RoundedButton):
    UNPRESSED_COLOR = StringProperty(get_color_from_hex("#A7A9AB"))
    PRESSED_COLOR = StringProperty(get_color_from_hex("#58585B"))
    FONT_COLOR = StringProperty(get_color_from_hex("#000000"))

