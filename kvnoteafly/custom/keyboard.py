import os

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.instructions import RenderContext
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.effectwidget import EffectWidget
from kivy.utils import get_color_from_hex

from custom.effects import ShaderTemplateMixin
from kivy.animation import Animation


class KeyboardLabelSeparatorOuter(Widget):
    background_color = get_color_from_hex("#0e0e0e")


class KeyboardLabelSeparatorInner(Label):
    background_color = get_color_from_hex("#0e0e0e")
    FONT_COLOR = "#eeeeee"
    FONT_SIZE = 36

    def __init__(self, **kwargs):
        markup_text = f"[color={self.FONT_COLOR}] + [/color]"
        super().__init__(text=markup_text, markup=True, font_size=self.FONT_SIZE, **kwargs)


class KeyboardImage(Image):
    pressed = BooleanProperty(False)

    def __init__(self, **kwargs):
        text = kwargs.pop('text')
        src = os.path.join("static", "keys", text.lower()) + ".png"
        super().__init__(source=src, **kwargs)

    def on_pressed(self, *args, **kwargs):
        animation_press = Animation(y=self.y - 7, duration=0.15, t='out_cubic')
        animation_press += Animation(y=self.y, duration=0.15, t='out_cubic')
        animation_press.start(self)


class KeyboardLabel(Label):
    background_color = get_color_from_hex("#eeeeee")
    FONT_COLOR = '#0e0e0e'
    FONT_SIZE = 36

    def __init__(self, **kwargs):
        markup_text = f"[color={self.FONT_COLOR}]{kwargs.pop('text')}[/color]"
        super(KeyboardLabel, self).__init__(text=markup_text, markup=True, font_size=self.FONT_SIZE,
                                            **kwargs)
