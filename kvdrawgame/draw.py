import random
import platform
import os
if 'debian' in platform.platform():
    os.environ['KIVY_GL_BACKEND'] = 'gl'
    os.environ['KIVY_AUDIO'] = 'sdl2'
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.graphics.instructions import InstructionGroup
from kivy.properties import NumericProperty
from kivy.utils import get_color_from_hex

colors = [
  "#FF355E",
  "#FD5B78",
  "#FF6037",
  "#FF9966",
  "#FF9933",
  "#FFCC33",
  "#FFFF66",
  "#FFFF66",
  "#CCFF00",
  "#66FF66",
  "#AAF0D1",
  "#50BFE6",
  "#FF6EFF",
  "#EE34D2",
  "#FF00CC",
  "#FF00CC",
  "#FF3855",
  "#FD3A4A",
  "#FB4D46",
  "#FA5B3D",
  "#FFAA1D",
  "#FFF700",
  "#299617",
  "#A7F432",
  "#2243B6",
  "#5DADEC",
  "#5946B2",
  "#9C51B6",
  "#A83731",
  "#AF6E4D",
  "#1B1B1B",
  "#BFAFB2",
  "#FF5470",
  "#FFDB00",
  "#FF7A00",
  "#FDFF00",
  "#87FF2A",
  "#0048BA",
  "#FF007C",
  "#E936A7"
]


class MyPaintWidget(Widget):

    MAX_LINES = NumericProperty(100)

    def on_touch_down(self, touch):
        line = self.make_line(touch)
        self.canvas.add(line)
        touch.ud['line'] = line

    def on_touch_move(self, touch):
        touch.ud['line'].children[2].points += [touch.x, touch.y]

    def on_touch_up(self, touch):
        self.trim_lines()

    def trim_lines(self):
        current_lines = self.canvas.get_group('line')[-self.MAX_LINES:]
        self.canvas.clear()
        for c in current_lines:
            self.canvas.add(c)

    def make_line(self, touch):
        c1 = self.bright_color()
        l1 = Line(points=(touch.x, touch.y), width=10)
        line = InstructionGroup(group='line')
        line.add(c1)
        line.add(l1)
        return line

    def bright_color(self):
        color_hex = random.choice(colors)
        color = Color(*get_color_from_hex(color_hex))
        return color


class MyPaintApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.painter = MyPaintWidget()

    def build(self):
        return self.painter


if __name__ == '__main__':
    MyPaintApp().run()
