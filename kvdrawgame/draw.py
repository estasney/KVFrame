import random
import platform
import os
import atexit
from datetime import datetime
import numpy as np

def enable_touch():
    os.system("xinput enable 'FT5406 memory based driver'")


if 'debian' in platform.platform():
    os.environ['KIVY_GL_BACKEND'] = 'gl'
    os.environ['KIVY_AUDIO'] = 'sdl2'
    os.system("xinput disable 'FT5406 memory based driver'")
    atexit.register(enable_touch)


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.graphics.instructions import InstructionGroup
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, ReferenceListProperty
from kivy.utils import get_color_from_hex
from kivy.clock import Clock


colors = ["#431dff", "#ffa11d", "#ff1100", "00ff44"]
points_f = 'points.txt'


class MyPaintWidget(Widget):

    MAX_LINES = NumericProperty(100)
    MAX_IDLE_SECONDS = 1
    NEW_COLOR_SECONDS = 30
    DEMO_REFRESH_RATIO = 0.04

    demo_travel = NumericProperty(0)
    demo_velocity_x = NumericProperty(0)
    demo_velocity_y = NumericProperty(0)
    demo_velocity = ReferenceListProperty(demo_velocity_x, demo_velocity_y)

    current_color = StringProperty(random.choice(colors))
    is_drawing = BooleanProperty(False)
    is_demo_mode = BooleanProperty(False)
    last_press = None

    def on_touch_down(self, touch):
        self.is_drawing = True
        self.is_demo_mode = False
        self.last_press = datetime.now()
        self.remove_demo_line()
        line = self.make_line(touch)
        self.canvas.add(line)
        touch.ud['line'] = line

    def on_touch_move(self, touch):
        touch.ud['line'].children[2].points += [touch.x, touch.y]


    def on_touch_up(self, touch):
        self.is_drawing = False
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

    def make_demo_line(self, x, y):
        c1 = self.bright_color()
        l1 = Line(points=(x, y), width=10)
        line = InstructionGroup(group='demo')
        line.add(c1)
        line.add(l1)
        return line

    def remove_demo_line(self):
        self.canvas.remove_group('demo')

    def check_demo_coverage(self, *args, **kwargs):
        line_ = self.canvas.get_group('demo')
        if not line_:
            return False

        if not self.is_demo_mode:
            return False


        line = line_[0].children[2]
        points = line.points

        a = np.array(list(zip(points[::2], points[1::2])))
        _, point_counts = np.unique(a, return_counts=True, axis=0)
        n_overlap = np.where(point_counts > 1)[0].size
        r_overlap = n_overlap / a.size
        print(r_overlap)
        if r_overlap >= self.DEMO_REFRESH_RATIO:
            self.remove_demo_line()
            self.demo_factory()
            return False

    def update_demo_line(self, *args):
        if self.is_demo_mode is False:
            return False

        line_ = self.canvas.get_group('demo')
        if not line_:
            return False
        line = line_[0].children[2]

        line_x, line_y = line.points[-2], line.points[-1]

        if line_y <= self.y:
            self.demo_velocity_y *= -1

        if line_y >= self.top:
            self.demo_velocity_y *= -1

        if line_x <= self.x:
            self.demo_velocity_x *= -1

        if line_x >= self.width:
            self.demo_velocity_x *= -1

        line.points += [(line_x + self.demo_velocity_x), (line_y + self.demo_velocity_y)]

    def demo_factory(self, interval=1/30, *args, **kwargs):

        x = self.width // random.randint(2, 10)
        y = self.height // random.randint(4, 12)
        velocity_x = random.randint(5, 10)
        sign_x = random.choice([1, -1])
        velocity_x *= sign_x

        velocity_y = random.randint(5, 10)
        sign_y = random.choice([1, -1])
        velocity_y *= sign_y

        self.demo_velocity_x = velocity_x
        self.demo_velocity_y = velocity_y

        demo_line = self.make_demo_line(x, y)
        self.canvas.add(demo_line)
        self.canvas.ask_update()
        Clock.schedule_interval(self.update_demo_line, interval)
        Clock.schedule_interval(self.check_demo_coverage, 1)

    def on_is_demo_mode(self, *args):
        # make a demo line
        if self.is_demo_mode:
            self.demo_factory()

    def bright_color(self):
        color = Color(*get_color_from_hex(self.current_color))
        return color

    def new_color(self, *args):
        possible = list(filter(lambda x: x != self.current_color, colors))
        self.current_color = random.choice(possible)

    def clear_screen(self, *args):
        if not self.last_press:
            self.last_press = datetime.now()

        nowtime = datetime.now()
        s = nowtime - self.last_press
        if s.seconds > self.MAX_IDLE_SECONDS:
            if not self.is_demo_mode and not self.is_drawing:
                self.canvas.clear()
                self.is_demo_mode = True


class MyPaintApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.painter = MyPaintWidget()

    def build(self):
        Clock.schedule_interval(self.painter.new_color, self.painter.NEW_COLOR_SECONDS)
        Clock.schedule_interval(self.painter.clear_screen, 1)
        return self.painter


if __name__ == '__main__':
    MyPaintApp().run()
