from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App

from utils import import_kv

import_kv(__file__)


class NoteAppScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current = 'chooser_screen'

    def category_selected(self, category):
        App.get_running_app().note_category = category.text

    def handle_app_display_state(self, app):
        if app.display_state == "choose":
            self.current = "chooser_screen"
        else:
            self.current = "note_screen2"

    def handle_notes(self, app):
        target = 'note_screen2' if self.current == 'note_screen1' else 'note_screen1'
        self.ids[target].set_note_content(app.note_data)
        self.current = target


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
