from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen


class NoteAppScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        self.current = 'note_screen1'

    def handle_notes(self, app):
        target = 'note_screen2' if self.current == 'note_screen1' else 'note_screen1'
        self.ids[target].set_note_content(app.note_data)
        self.current = target


class NoteScreen(Screen):
    current_note = ObjectProperty()

    def set_note_content(self, note_data: dict):
        self.current_note.set_note_content(note_data)
