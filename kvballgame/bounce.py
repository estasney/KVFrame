import platform
import os
if 'debian' in platform.platform():
    os.environ['KIVY_GL_BACKEND'] = 'gl'
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, StringProperty, ListProperty
from kivy.vector import Vector
from kivy.core.image import Image
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from math import log
import glob
import random
import os


class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    spin_rate = NumericProperty(0)
    angle = NumericProperty(0)

    sound = SoundLoader.load(os.path.realpath("resources/audio/boing.wav"))

    ball_texture = ObjectProperty()
    ball_texture_path = StringProperty()

    def reload_texture(self, *args, **kwargs):
        image = Image(os.path.realpath(self.ball_texture_path))
        self.ball_texture = image.texture
        self.canvas.ask_update()

    def on_ball_texture_path(self, *args, **kwargs):
        self.reload_texture(self)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        if abs(self.velocity_x) > 1 or abs(self.velocity_y) > 1:
            self.angle += log(max([abs(self.velocity_x), abs(self.velocity_y)]))



    def decay(self, *args, **kwargs):

        self.velocity_x *= 0.9
        self.velocity_y *= 0.9

    def boing(self):
        vx = random.randint(10, 25)
        vy = random.randint(10, 25)
        vz = random.randint(10, 25)
        dx = random.choice([1, -1])
        dy = random.choice([1, -1])
        dz = random.choice([1, -1])

        self.velocity_x += (vx * dx)
        self.velocity_y += (vy * dy)
        self.sound.play()

    def on_angle(self, item, angle):
        if angle >= 360:
            item.angle = 0


class BounceGame(Widget):

    ball = ObjectProperty(None)
    ball_textures = glob.glob("resources/images/balls/*.png")

    def random_chance(self, low, high):
        r = random.randrange(low, high)
        if r == low:
            return True
        else:
            return False

    def find_new_texture(self):
        current_texture = self.ball.ball_texture_path
        new_textures = [t for t in self.ball_textures if t != current_texture]
        return random.choice(new_textures)

    def serve_ball(self, vel=(4, 0)):
        self.ball.ball_texture_path = self.ball_textures[0]
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= 1.1
            self.ball.velocity_y *= -1

        if (self.ball.x < self.x) or ((self.ball.x + self.ball.width) > self.width):
            self.ball.velocity_x *= 1.1
            self.ball.velocity_x *= -1

    def on_touch_down(self, touch):
        if self.ball.collide_point(touch.x, touch.y):
            self.ball.boing()
            do_texture_change = self.random_chance(0, 2)
            if do_texture_change:
                self.ball.ball_texture_path = self.find_new_texture()


class BounceApp(App):
    def build(self):
        game = BounceGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        Clock.schedule_interval(game.ball.decay, 0.1)
        return game


if __name__ == '__main__':
    BounceApp().run()