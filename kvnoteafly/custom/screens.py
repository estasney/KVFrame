from itertools import cycle

from cytoolz import sliding_window
from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from utils import import_kv

import_kv(__file__)


class NoteAppScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current = 'chooser_screen'
        self.note_screen_cycler = sliding_window(2, cycle([1, 2]))
        self.last_note_screen = None

    def category_selected(self, category):
        App.get_running_app().note_category = category.text

    def handle_app_display_state(self, app):
        if app.display_state == "choose":  # Show the Category Selection Screen
            self.current = "chooser_screen"
        else:
            self.handle_notes(app)

    def handle_notes(self, app):
        last_active, next_active = next(self.note_screen_cycler)
        target = f"note_screen{next_active}"
        self.ids[target].set_note_content(app.note_data)
        self.current = target
        self.last_note_screen = next_active


class NoteCategoryChooserScreen(Screen):
    chooser_object = ObjectProperty()
    manager = ObjectProperty()
    categories = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def category_selected(self, category):
        self.manager.category_selected(category)


class NoteCategoryScreen(Screen):
    current_note = ObjectProperty()

    def set_note_content(self, note_data: dict):
        self.current_note.set_note_content(note_data)
