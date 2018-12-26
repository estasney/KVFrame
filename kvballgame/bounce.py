import platform
import os
if 'debian' in platform.platform():
    os.environ['KIVY_GL_BACKEND'] = 'gl'
    os.environ['KIVY_AUDIO'] = 'sdl2'
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

    x_decay = NumericProperty(0.99)
    y_decay = NumericProperty(-0.95)

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

    def get_resultant_vector(self, touch):
        col_vector = Vector(touch.pos) - Vector(self.center)
        col_vector_mag = col_vector.length()
        random_magnitude = random.randint(5, 10)

        return random_magnitude / col_vector * col_vector_mag


    def move(self):

        if self.y <= self.parent.y:

            if self.y < self.parent.y:
                self.pos = Vector(0, self.parent.y - self.y) + self.pos
            if abs(self.velocity_y) < (8 * abs(self.y_decay)):
                self.velocity_y = 0
                self.y_decay = 0
            else:
                self.velocity_y *= -0.8

        if self.top >= self.parent.top:

            if self.top > self.parent.top:
                self.pos = Vector(0, self.parent.top - self.top) + self.pos
            self.velocity_y = abs(self.velocity_y) * 0.8 * -1

        if self.x <= self.parent.x:

            if self.x < self.parent.x:
                self.pos = Vector(self.parent.x - self.x + 3, 0) + self.pos
            self.velocity_x *= -0.8

        if (self.x + self.width) >= self.parent.width:

            if (self.x + self.width) > self.parent.width:
                self.pos = Vector(self.parent.width - self.x - self.width - 3, 0) + self.pos
            self.velocity_x *= -0.8


        self.pos = Vector(*self.velocity) + self.pos

        if abs(self.velocity_x) > 1 or abs(self.velocity_y) > 1:
            self.angle += log(max([abs(self.velocity_x), abs(self.velocity_y)]))

        self.decay()

    def decay(self, *args, **kwargs):

        self.velocity_x *= self.x_decay
        self.velocity_y += self.y_decay
        

    def boing(self, touch):

        resultant_vector = self.get_resultant_vector(touch)
        print(resultant_vector)

        self.velocity_x += resultant_vector[0]
        self.velocity_y += resultant_vector[1]
        self.y_decay = -0.95
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

    def serve_ball(self, vel=(4, 4)):
        self.ball.ball_texture_path = random.choice(self.ball_textures)
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):

        self.ball.move()



    def on_touch_down(self, touch):
        if self.ball.collide_point(touch.x, touch.y):
            self.ball.boing(touch)
            do_texture_change = self.random_chance(0, 2)
            if do_texture_change:
                self.ball.ball_texture_path = self.find_new_texture()

    def on_touch_move(self, touch):

        if self.ball.collide_point(touch.x, touch.y):
            self.ball.boing(touch)
            do_texture_change = self.random_chance(0, 2)
            if do_texture_change:
                self.ball.ball_texture_path = self.find_new_texture()


class BounceApp(App):
    def build(self):
        game = BounceGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1/60)

        return game


if __name__ == '__main__':
    BounceApp().run()
