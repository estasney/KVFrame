import os
import threading

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.core.audio import SoundLoader
from kivy.properties import *

from kvarcade.input import SN74LS165


class Arcade(App):
    APP_NAME = "Arcade"

    SOUND_0 = SoundLoader.load(os.path.realpath("resources/audio/Cars/Engine/Mustang.wav"))
    SOUND_1 = SoundLoader.load(os.path.realpath("resources/audio/Cars/Engine/Mustang.wav"))
    SOUND_2 = SoundLoader.load(os.path.realpath("resources/audio/Cars/Engine/Mustang.wav"))
    SOUND_3 = SoundLoader.load(os.path.realpath("resources/audio/Cars/Engine/Mustang.wav"))
    SOUND_4 = SoundLoader.load(os.path.realpath("resources/audio/Cars/Engine/Mustang.wav"))
    SOUND_5 = SoundLoader.load(os.path.realpath("resources/audio/Cars/Engine/Mustang.wav"))
    SOUND_6 = SoundLoader.load(os.path.realpath("resources/audio/Cars/Engine/Mustang.wav"))
    SOUND_7 = SoundLoader.load(os.path.realpath("resources/audio/Cars/Engine/Mustang.wav"))

    button_0 = BooleanProperty()
    button_1 = BooleanProperty()
    button_2 = BooleanProperty()
    button_3 = BooleanProperty()
    button_4 = BooleanProperty()
    button_5 = BooleanProperty()
    button_6 = BooleanProperty()
    button_7 = BooleanProperty()

    def run_threaded(self, target_function, *args, **kwargs):
        threading.Thread(target=target_function, args=args, kwargs=kwargs).start()

    def _on_button(self, sound_num):
        sound = getattr(self, "SOUND_{}".format(sound_num))
        is_stopped = sound.get_pos() == 0
        if is_stopped:
            sound.play()
        else:
            sound.stop()

    def on_button_0(self, *args, **kwargs):
        self._on_button(0)

    def on_button_1(self, *args, **kwargs):
        self._on_button(1)

    def on_button_2(self, *args, **kwargs):
        self._on_button(2)

    def on_button_3(self, *args, **kwargs):
        self._on_button(3)

    def on_button_4(self, *args, **kwargs):
        self._on_button(4)

    def on_button_5(self, *args, **kwargs):
        self._on_button(5)

    def on_button_6(self, *args, **kwargs):
        self._on_button(6)

    def on_button_7(self, *args, **kwargs):
        self._on_button(7)

    def _setup_input(self):
        self.input_provider = SN74LS165()

    def get_input_state(self):
        is_high = self.input_provider.poll()
        for i in range(8):
            btn_atr = "BUTTON_" + str(i)
            setattr(self, btn_atr, i in is_high)

    def build(self):
        self._setup_input()
        Clock.schedule_interval(self.get_input_state, 0.01)

if __name__ == '__main__':
    Arcade().run()
