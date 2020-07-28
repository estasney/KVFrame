import os

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex


class KeyboardLabelSeparatorOuter(Widget):
    background_color = get_color_from_hex("#0e0e0e")


class KeyboardLabelSeparatorInner(Label):
    background_color = get_color_from_hex("#0e0e0e")
    FONT_COLOR = "#eeeeee"
    FONT_SIZE = 24

    def __init__(self, **kwargs):
        markup_text = f"[color={self.FONT_COLOR}] + [/color]"
        super().__init__(text=markup_text, markup=True, font_size=self.FONT_SIZE, **kwargs)


class KeyboardImage(Image):

    def __init__(self, **kwargs):
        text = kwargs.pop('text')
        src = os.path.join("static", "keys", text.lower()) + ".png"
        super(KeyboardImage, self).__init__(source=src, **kwargs)


class KeyboardLabel(Label):
    background_color = get_color_from_hex("#eeeeee")
    FONT_COLOR = '#0e0e0e'
    FONT_SIZE = 24

    def __init__(self, **kwargs):
        markup_text = f"[color={self.FONT_COLOR}]{kwargs.pop('text')}[/color]"
        super(KeyboardLabel, self).__init__(text=markup_text, markup=True, font_size=self.FONT_SIZE,
                                            **kwargs)