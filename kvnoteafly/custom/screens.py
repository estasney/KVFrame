from itertools import cycle

from toolz import sliding_window
from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty, OptionProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from utils import import_kv

import_kv(__file__)


class NoteAppScreenManager(ScreenManager):

    app = ObjectProperty()
    play_state = StringProperty()

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.current = 'chooser_screen'
        self.note_screen_cycler = sliding_window(2, cycle([1, 2]))
        self.last_note_screen = None
        self.app = app
        self.app.bind(display_state=self.handle_app_display_state)
        self.app.bind(play_state=self.handle_app_play_state)

    def category_selected(self, category):
        App.get_running_app().note_category = category.text

    def handle_app_display_state(self, instance, new):
        if new == "choose":  # Show the Category Selection Screen
            self.current = "chooser_screen"
        elif new == "display":
            self.handle_notes()
        elif new == "list":
            self.handle_notes_list_view()
        else:
            raise Exception(f"Unhandled display state {new}")

    def handle_app_play_state(self, instance, value):
        self.play_state = value

    def handle_notes(self, *args, **kwargs):
        last_active, next_active = next(self.note_screen_cycler)
        target = f"note_screen{next_active}"
        self.ids[target].set_note_content(self.app.note_data)
        self.current = target
        self.last_note_screen = next_active

    def handle_notes_list_view(self, *args, **kwargs):
        self.ids['list_view_screen'].set_note_list_view()
        self.current = 'list_view_screen'


class NoteCategoryChooserScreen(Screen):
    child_object = ObjectProperty()
    categories = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def category_selected(self, category):
        self.manager.category_selected(category)


class NoteCategoryScreen(Screen):
    current_note = ObjectProperty()

    def set_note_content(self, note_data: dict):
        self.current_note.set_note_content(note_data)

class NoteListViewScreen(Screen):
    child_object = ObjectProperty()
    notes = ListProperty()

    def set_note_list_view(self, *args, **kwargs):
        self.ids['scroller'].set(self.notes)
