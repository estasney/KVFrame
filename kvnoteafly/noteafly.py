import string
import sys
import os
import random
from itertools import combinations_with_replacement

import numpy as np
import requests
from colour import Color
from dotenv import load_dotenv
import threading
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import *

from kvnoteafly.custom import *


class NoteAFly(App):
    APP_NAME = 'NoteAFly'

    screen_manager = ObjectProperty()
    session = None
    bg_color_r = NumericProperty(0)
    bg_color_g = NumericProperty(0)
    bg_color_b = NumericProperty(0)
    bg_color = ReferenceListProperty(bg_color_r, bg_color_g, bg_color_b)
    clock_time = StringProperty()
    note_data = DictProperty(rebind=True)
    colors = DictProperty({
        "Light":   (0.3843137254901961, 0.4470588235294118, 0.4823529411764706),
        "Primary": (0.21568627450980393, 0.2784313725490195, 0.30980392156862746),
        "Dark":    (0.06274509803921569, 0.1254901960784313, 0.15294117647058825),
        "Accent1": (0.8588235294117648, 0.227450980392157, 0.20392156862745092),
        "Accent2": (0.02352941176470591, 0.8392156862745098, 0.6274509803921572)
        })

    def run_threaded(self, target_function, *args, **kwargs):
        threading.Thread(target=target_function, args=args, kwargs=kwargs).start()

    def _update_property(self, property_name, value):
        setattr(self, property_name, value)

    def _setup_session(self):
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 '
                          'Safari/537.36 '
            })
        self.session = session

    def get_time(self, *args, **kwargs):
        self.clock_time = datetime.strftime(datetime.now(), "%I:%M %p")

    def update_current_note(self, *args, **kwargs):
        d = dict(
                note_title='Test',
                note_text=f"{''.join(random.choices(string.ascii_lowercase, k=4))}"
                )
        self._update_property("note_data", d)


    def on_note_data(self, *args, **kwargs):
        self.screen_manager.create_notes(self)

    def build(self):
        self._setup_session()
        self.get_time()

        sm = NoteAppScreenManager()
        self.screen_manager = sm
        sm.create_notes(app=self)
        Clock.schedule_interval(self.get_time, 10)
        Clock.schedule_interval(self.update_current_note, 0.25)
        return sm


if __name__ == '__main__':
    sys.path.append(os.getcwd())
    load_dotenv()
    NoteAFly().run()
