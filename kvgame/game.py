from kivy.app import App
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy import event
import os
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.slider import Slider
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
from functools import partial


class GameApp(App):
    sound_enabled = BooleanProperty(False)
    sounds = {}

    def get_path(self, fp):
        return os.path.realpath(fp)

    def global_check(self, toggle=None):
            if not toggle:
                return self.sound_enabled

            if self.sound_enabled is True:
                self.stop_all_sounds()
                self.sound_enabled = False
            else:
                self.sound_enabled = True
            return self.sound_enabled


    def stop_all_sounds(self):
        [s.stop() for s in list(self.sounds.values())]


    def sound(self, *args, **kwargs):
        global_toggle = kwargs.get('global_toggle', None)
        do_sound = self.global_check(global_toggle)
        widget_callback = kwargs.get('callback', None)
        sound_key = kwargs['key']

        if not do_sound:
            if widget_callback:
                widget_callback()
            return None

        widget_sound = self.sounds[sound_key]
        play_sound = widget_callback()
        if play_sound:
            do_loop = kwargs.get('loop', False)
            widget_sound.play()
            if do_loop:
                widget_sound.loop = True
        else:
            widget_sound.stop()

    def receive_sound(self, key, sound):
        self.sounds[key] = sound




class IconHolder(FloatLayout):
    pass


class Icon(ButtonBehavior, Image):
    src_normal = None
    src_pressed = None
    sound_src = None


    def __init__(self, **kwargs):
        super(Icon, self).__init__(**kwargs)
        if self.sound_src:
            self.load_sound()

    def load_sound(self):
        if self.sound_src:
            s = SoundLoader.load(self.sound_src)
            a = App.get_running_app()
            a.receive_sound(self.__class__.__name__, s)

    def callback(self, *args, **kwargs):
        if self.source == self.src_pressed:
            self.source = self.src_normal
        else:
            self.source = self.src_pressed


class KeyIcon(Icon):
    src_normal = os.path.realpath("resources/images/key_off.png")
    src_pressed = os.path.realpath("resources/images/key_on.png")

    sound_src = os.path.realpath("resources/audio/engine_start.wav")
    looping_src = os.path.realpath("resources/audio/idle.wav")

    def __init__(self, **kwargs):
        super(KeyIcon, self).__init__(**kwargs)
        if self.sound_src:
            self.load_sound()

    def load_sound(self):
        ignition_sound = SoundLoader.load(self.sound_src)
        idle_sound = SoundLoader.load(self.looping_src)
        a = App.get_running_app()
        sound_key_ignition = self.__class__.__name__ + "_ignition"
        sound_key_idle = self.__class__.__name__ + "_idle"
        a.receive_sound(sound_key_idle, idle_sound)
        a.receive_sound(sound_key_ignition, ignition_sound)

    def play_loop(self, *args, **kwargs):
        a = App.get_running_app()
        a.sound(global_toggle=None, key="KeyIcon_idle", callback=lambda: True)

    def callback(self, *args, **kwargs):
        if self.source == self.src_normal:
            self.source = self.src_pressed
            Clock.schedule_once(self.play_loop, 3)
            return True
        else:
            self.source = self.src_normal
            return False


class SpeedSlider(Slider):
    cursor_src = os.path.realpath('resources/images/slider_handle.png')
    sound_increase_src = os.path.realpath('resources/audio/engine_accelerate.wav')
    sound_decrease_src = os.path.realpath('resources/audio/engine_deaccelerate.wav')
    last_value = 0
    sound_increase = None
    sound_decrease = None

    def __init__(self, **kwargs):
        super(SpeedSlider, self).__init__(**kwargs)
        self.load_sound()

    def load_sound(self):
        sound_increase = SoundLoader.load(self.sound_increase_src)
        sound_increase_key = 'SpeedSlider_increase'
        sound_decrease = SoundLoader.load(self.sound_decrease_src)
        sound_decrease_key = 'SpeedSlider_decrease'
        a = App.get_running_app()
        a.receive_sound(sound_increase_key, sound_increase)
        a.receive_sound(sound_decrease_key, sound_decrease)


    def callback(self, *args, **kwargs):
        # is movement increasing or decreasing?
        if self.value > self.last_value:
            self.last_value = self.value
            self.increasing()
        elif self.value < self.last_value:
            self.last_value = self.value
            self.decreasing()

    def increasing(self):
        a = App.get_running_app()
        a.sound(key="SpeedSlider_decrease", callback=lambda: False)  # stop decrease from playing
        a.sound(key="SpeedSlider_increase", callback=lambda: True)

    def decreasing(self):
        a = App.get_running_app()
        a.sound(key="SpeedSlider_increase", callback=lambda: False)
        a.sound(key="SpeedSlider_increase", callback=lambda: True)



if __name__ == "__main__":

    GameApp().run()
