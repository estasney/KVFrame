import os

os.environ['KIVY_AUDIO'] = 'sdl2'
import threading
import sys

sys.path.append("/home/pi/Desktop/KVFrame")
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import BooleanProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager

from kvarcade.input import SN74LS165
from kvarcade.player import SoundCycler


class Arcade(App):
    APP_NAME = "Arcade"

    SOUND_0 = SoundCycler(os.path.realpath("resources/audio/Trains"))
    SOUND_1 = SoundCycler(os.path.realpath("resources/audio/Sirens"))
    SOUND_2 = SoundCycler(os.path.realpath("resources/audio/Cars/Engine"))
    SOUND_3 = SoundCycler(os.path.realpath("resources/audio/Cars/Race"))
    SOUND_4 = SoundCycler(os.path.realpath("resources/audio/Cars/Narrated"))
    SOUND_5 = SoundCycler(os.path.realpath("resources/audio/Submarine"))
    SOUND_6 = SoundCycler(os.path.realpath("resources/audio/Noise/Construction"))
    SOUND_7 = SoundCycler(os.path.realpath("resources/audio/Planes"))

    button_0 = BooleanProperty(False)
    button_1 = BooleanProperty(False)
    button_2 = BooleanProperty(False)
    button_3 = BooleanProperty(False)
    button_4 = BooleanProperty(False)
    button_5 = BooleanProperty(False)
    button_6 = BooleanProperty(False)
    button_7 = BooleanProperty(False)

    def run_threaded(self, target_function, *args, **kwargs):
        threading.Thread(target=target_function, args=args, kwargs=kwargs).start()

    def _on_button(self, sound_num, *args):
        _, new_value = args
        sound = getattr(self, "SOUND_{}".format(sound_num))
        if new_value:
            # print("Playing sound for : {}".format(sound_num))
            sound.play()
            sound.seek(0)
        else:
            # print("Stopping sound for {}".format(sound_num))
            sound.stop()

    def on_button_0(self, *args, **kwargs):
        self._on_button(0, *args)

    def on_button_1(self, *args, **kwargs):
        self._on_button(1, *args)

    def on_button_2(self, *args, **kwargs):
        self._on_button(2, *args)

    def on_button_3(self, *args, **kwargs):
        self._on_button(3, *args)

    def on_button_4(self, *args, **kwargs):
        self._on_button(4, *args)

    def on_button_5(self, *args, **kwargs):
        self._on_button(5, *args)

    def on_button_6(self, *args, **kwargs):
        self._on_button(6, *args)

    def on_button_7(self, *args, **kwargs):
        self._on_button(7, *args)

    def _setup_input(self):
        self.input_provider = SN74LS165()

    def get_input_state(self, *args, **kwargs):
        is_high = self.input_provider.poll()
        for i in range(8):
            btn_atr = "button_{}".format(i)
            current_state = getattr(self, btn_atr)
            new_state = i in is_high
            if current_state != new_state:
                setattr(self, btn_atr, new_state)

    def build(self):
        self._setup_input()
        self.sm = ScreenManager()
        Clock.schedule_interval(self.get_input_state, 0.01)
        return self.sm


if __name__ == '__main__':
    Arcade().run()
