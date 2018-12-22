from kivy.app import App
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import os
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty
from kivy.uix.slider import Slider
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
from functools import partial

class IconHolder(FloatLayout):
    pass


class Icon(ButtonBehavior, Image):
    src_normal = None
    src_pressed = None
    sound_src = None

    def callback(self, *args, **kwargs):
        if not kwargs:
            self.source = self.src_pressed
            self.play_sound()
        else:
            self.source = kwargs['img_src']

    def play_sound(self, *args, **kwargs):
        if not getattr(self, 'sound_src', None):
            Clock.schedule_once(partial(self.callback, img_src=self.src_normal), 1)
            return
        if not kwargs:
            sound = SoundLoader.load(self.sound_src)
            sound.play()
            Clock.schedule_once(partial(self.callback, img_src=self.src_normal), sound.length)


class SpeedSlider(Slider):
    cursor_src = os.path.realpath('resources/images/slider_handle.png')
    sound_increase_src = os.path.realpath('resources/audio/engine_accelerate.wav')
    sound_decrease_src = os.path.realpath('resources/audio/engine_deaccelerate.wav')
    last_value = 0
    sound_increase = None
    sound_decrease = None

    def callback(self, *args, **kwargs):
        # is movement increasing or decreasing?
        if self.value > self.last_value:
            self.last_value = self.value
            self.increasing()
        elif self.value < self.last_value:
            self.last_value = self.value
            self.decreasing()

    def increasing(self):
        if not self.sound_increase:
            self.sound_increase = SoundLoader.load(self.sound_increase_src)
        if not self.sound_decrease:
            self.sound_decrease = SoundLoader.load(self.sound_decrease_src)

        if not App.get_running_app().sound_enabled:
            return

        if self.sound_increase.state == 'play':
            return
        if self.sound_decrease.state == 'play':
            self.sound_decrease.stop()
        self.sound_increase.play()



    def decreasing(self):
        if not self.sound_increase:
            self.sound_increase = SoundLoader.load(self.sound_increase_src)
        if not self.sound_decrease:
            self.sound_decrease = SoundLoader.load(self.sound_decrease_src)

        if not App.get_running_app().sound_enabled:
            return

        if self.sound_decrease.state == 'play':
            return
        if self.sound_increase.state == 'play':
            self.sound_increase.stop()
        self.sound_decrease.play()




class KeyIcon(Icon):
    src_normal = os.path.realpath("resources/images/key_off.png")
    src_pressed = os.path.realpath("resources/images/key_on.png")
    sound_src = os.path.realpath("resources/audio/engine_start.wav")

    looping_audio = None
    looping_src = os.path.realpath("resources/audio/idle.wav")

    def toggle_inition(self):
        if self.source == self.src_normal:
            self.source = self.src_pressed
            App.get_running_app().sound_enabled = True
            self.play_sound()
        else:
            self.source = self.src_normal
            App.get_running_app().sound_enabled = False
        self.toggle_looping()


    def play_sound(self, *args, **kwargs):
        sound = SoundLoader.load(self.sound_src)
        sound.play()



    def toggle_looping(self):
        if self.looping_audio and self.looping_audio.state == 'play':
            self.looping_audio.stop()
            return
        elif self.looping_audio and self.looping_audio.state == 'stop':
            self.looping_audio.play()
            return
        self.looping_audio = SoundLoader.load(self.looping_src)
        self.looping_audio.loop = True
        self.looping_audio.play()


class GameApp(App):
    sound_enabled = BooleanProperty(default=False)


if __name__ == "__main__":

    GameApp().run()
