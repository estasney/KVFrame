import string
import sys
import os
import random
import requests

from dotenv import load_dotenv
import threading
from itertools import cycle
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import *

from custom.screens import NoteAppScreenManager
from db import create_session, Note


class NoteAFly(App):
    APP_NAME = 'NoteAFly'

    session = None
    n_notes = 0
    note_idx = 0
    notes_data = None

    screen_manager = ObjectProperty()

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
        self.session = create_session()

    def _setup_data(self):
        n_notes = self.session.query(Note).count()
        self.n_notes = n_notes
        self.notes_data = [note.to_tuple() for note in self.session.query(Note).all()]
        self.note_idx = cycle(range(self.n_notes - 1))

    def get_time(self, *args, **kwargs):
        self.clock_time = datetime.strftime(datetime.now(), "%I:%M %p")

    def update_current_note(self, *args, **kwargs):
        note = self.notes_data[next(self.note_idx)]

        d = dict(
                note_title=note.note_title,
                note_text=note.note_text,
                kbd_buttons=note.kbd_buttons
                )
        self._update_property("note_data", d)

    def on_note_data(self, *args, **kwargs):
        self.screen_manager.create_notes(self)

    def build(self):
        self._setup_session()
        self._setup_data()
        self.get_time()
        sm = NoteAppScreenManager()
        self.screen_manager = sm
        sm.create_notes(app=self)
        Clock.schedule_once(self.update_current_note)
        Clock.schedule_interval(self.get_time, 10)
        Clock.schedule_interval(self.update_current_note, 5)
        return sm


if __name__ == '__main__':
    sys.path.append(os.getcwd())
    load_dotenv()
    NoteAFly().run()
