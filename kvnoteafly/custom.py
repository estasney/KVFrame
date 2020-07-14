from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, DictProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.uix.widget import Widget


class Separator(Widget):
    pass


class HSeparator(Separator):
    pass


class VSeparator(Separator):
    pass


class NoteTitle(BoxLayout):
    title_text = StringProperty()

    def __init__(self, **kwargs):
        if 'note_title' in kwargs:
            self.title_text = kwargs.pop('note_title')
        super().__init__(**kwargs)

    def set(self, **kwargs):
        if 'note_title' in kwargs:
            self.title_text = kwargs.pop('note_title')


class Note(BoxLayout):

    note_title = ObjectProperty()
    note_content = ObjectProperty()
    note_tags = ObjectProperty()

    def set_note_content(self, **kwargs):
        self.note_title.set(**kwargs)
        self.note_content.set(**kwargs)
        # self.note_tags.set(**kwargs)

class NoteContent(BoxLayout):
    note_text = StringProperty()

    def __init__(self, **kwargs):
        if 'note_text' in kwargs:
            self.note_text = kwargs.pop('note_text')
        super().__init__(**kwargs)

    def set(self, **kwargs):
        if 'note_text' in kwargs:
            self.note_text = kwargs.pop("note_text")


class NoteTags(BoxLayout):
    pass


class NoteScreen(Screen):
    current_note = ObjectProperty()

    def set_note_content(self, **kwargs):
        self.current_note.set_note_content(**kwargs)


class NoteAppScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        self.current = 'note_screen'

    def create_notes(self, app):
        self.ids['note_screen'].set_note_content(**app.note_data)

    def on_touch_down(self, touch):
        pass
