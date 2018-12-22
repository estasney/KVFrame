from kivy.app import App
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
from functools import partial

class IconHolder(GridLayout):
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


class StopIcon(Icon):
    src_normal = os.path.realpath("resources/images/stopsign.png")
    src_pressed = os.path.realpath("resources/images/stopsign_pressed.png")
    sound_src = os.path.realpath("resources/audio/skid.wav")

class GoIcon(Icon):
    src_normal = os.path.realpath("resources/images/go.png")
    src_pressed = os.path.realpath("resources/images/go_pressed.png")
    sound_src = os.path.realpath("resources/audio/go.wav")


class KeyIcon(Icon):
    src_normal = os.path.realpath("resources/images/key_off.png")
    src_pressed = os.path.realpath("resources/images/key_on.png")
    sound_src = os.path.realpath("resources/audio/engine_start.wav")

    looping_audio = None
    looping_src = os.path.realpath("resources/audio/idle.wav")

    def toggle_inition(self):
        if self.source == self.src_normal:
            self.source = self.src_pressed
            self.play_sound()
        else:
            self.source = self.src_normal
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
    pass

if __name__ == "__main__":

    GameApp().run()
