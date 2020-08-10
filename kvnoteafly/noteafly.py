
import sys
import os
from dotenv import load_dotenv
import threading
from itertools import cycle
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (OptionProperty, ObjectProperty, ListProperty, StringProperty, DictProperty)

from custom.screens import NoteAppScreenManager
from db import create_session, Note


class NoteAFly(App):
    """
    Attributes
    ----------
    db_session
        session used for database
    note_idx
        Uses itertools `cycle` so that calling `next` will yield the next valid index
    notes_data
        All notes
    notes_data_categorical
        All notes that are a Category == `self.note_category`
    note_categories: ListProperty
        List of all note categories
    note_category: StringProperty
        The Note category currently active
    note_data: DictProperty
        Data regarding the currently displayed note
    schedulers: DictProperty
        Holds previously called schedulers
    display_state: OptionProperty
        One of [Display, Choose]
        Choose:: Display all known categories
        Display:: Iterate through notes matching `self.note_category`
    screen_manager: ObjectProperty
        Holds the reference to ScreenManager
    colors: DictProperty
        Color scheme

    """

    APP_NAME = 'NoteAFly'

    db_session = None

    note_idx = None
    notes_data = None
    notes_data_categorical = None
    note_categories = ListProperty()
    note_category = StringProperty('')
    note_data = DictProperty(rebind=True)

    next_note_scheduler = ObjectProperty()

    display_state = OptionProperty("choose", options=["choose", "display"])
    play_state = OptionProperty("play", options=["play", "pause"])

    screen_manager = ObjectProperty()

    colors = DictProperty({
        "Light":   (0.3843137254901961, 0.4470588235294118, 0.4823529411764706),
        "Primary": (0.21568627450980393, 0.2784313725490195, 0.30980392156862746),
        "Dark":    (0.06274509803921569, 0.1254901960784313, 0.15294117647058825),
        "Accent1": (0.8588235294117648, 0.227450980392157, 0.20392156862745092),
        "Accent2": (0.02352941176470591, 0.8392156862745098, 0.6274509803921572)
        })

    def run_threaded(self, target_function, *args, **kwargs):
        """Run a function in a separate thread"""
        threading.Thread(target=target_function, args=args, kwargs=kwargs).start()

    def _update_property(self, property_name, value):
        """Intended for updating a property in a separate thread"""
        setattr(self, property_name, value)

    def _setup_data(self):
        """Initial load of data"""
        self.db_session = create_session()
        self.notes_data = [note.to_dict() for note in self.db_session.query(Note).all()]
        self.note_categories = list(set([note_dict['category'] for note_dict in self.notes_data]))

    def toggle_play_state(self, *args, **kwargs):
        if self.play_state == "play":
            self.play_state = "pause"
        else:
            self.play_state = "play"

    def next_note(self, *args, **kwargs):
        """Update `self.note_data` from `self.notes_data`"""
        note = self.notes_data_categorical[next(self.note_idx)]
        self.note_data = note

    def on_play_state(self, instance, value):
        if value == "pause":
            self.next_note_scheduler.cancel()
        else:
            self.next_note_scheduler()

    def on_note_category(self, instance, value):
        if not value:
            self.notes_data_categorical = []
            self.note_idx = None
            if self.next_note_scheduler:
                self.next_note_scheduler.cancel()
            self.display_state = "choose"
        else:

            self.notes_data_categorical = [note for note in self.notes_data if note['category'] == value]
            self.note_idx = cycle(range(len(self.notes_data_categorical)))
            if not self.next_note_scheduler:
                self.next_note_scheduler = Clock.schedule_interval(self.next_note, 5)
            else:
                self.next_note_scheduler()
            self.next_note()
            self.display_state = "display"

    def on_note_data(self, *args, **kwargs):
        self.screen_manager.handle_notes(self)

    def build(self):
        self._setup_data()
        sm = NoteAppScreenManager(self)
        self.screen_manager = sm
        return sm


if __name__ == '__main__':
    sys.path.append(os.getcwd())
    load_dotenv()
    NoteAFly().run()
