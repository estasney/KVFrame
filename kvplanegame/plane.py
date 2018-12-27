import platform
import os

if 'debian' in platform.platform():
    os.environ['KIVY_GL_BACKEND'] = 'gl'
    os.environ['KIVY_AUDIO'] = 'sdl2'
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, \
    ObjectProperty, StringProperty, ListProperty, BooleanProperty, DictProperty
from kivy.vector import Vector
from kivy.core.image import Image
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from functools import partial
from math import log
import glob
import random
import os
import numpy as np


class Plane(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)


    angle = NumericProperty(0)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def take_off(self):
        anim = Animation(x=self.x+150, duration=3)


        def start_anim1(animation, widget):
            anim1 = Animation(x=self.x + 150, y=self.y + 300, duration=3)
            anim1.start(self)

        anim.bind(on_complete=start_anim1)
        anim.start(self)


        










class PlaneGame(Widget):
    plane = ObjectProperty(None)

    def update(self, dt):

        self.plane.move()

    def on_touch_down(self, touch):
        self.plane.take_off()



class PlaneApp(App):
    def build(self):
        game = PlaneGame()
        Clock.schedule_interval(game.update, 1 / 60)

        return game


if __name__ == '__main__':
    PlaneApp().run()
