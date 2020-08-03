from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from utils import import_kv

import_kv(__file__)


class NoteAppScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def on_touch_down(self, touch):
    #     self.current = 'note_screen1'

    def testing_chooser(self):
        self.current = 'chooser_screen'
        self.ids[self.current].set_categories(['A', 'B'])

    def handle_notes(self, app):
        target = 'note_screen2' if self.current == 'note_screen1' else 'note_screen1'
        self.ids[target].set_note_content(app.note_data)
        self.testing_chooser()


class NoteCategoryChooserScreen(Screen):
    chooser_object = ObjectProperty()
    manager = ObjectProperty()

    def set_categories(self, categories):
        self.chooser_object.set_categories(categories)

    def category_selected(self, category):
        self.manager.current = 'note_screen1'


class NoteCategoryScreen(Screen):
    current_note = ObjectProperty()

    def set_note_content(self, note_data: dict):
        self.current_note.set_note_content(note_data)
