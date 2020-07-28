from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout

from custom.keyboard import KeyboardLabelSeparatorOuter, KeyboardLabelSeparatorInner, KeyboardImage


class Note(BoxLayout):
    note_title = ObjectProperty()
    note_content = ObjectProperty()
    note_tags = ObjectProperty()

    def set_note_content(self, **kwargs):
        self.note_title.set(**kwargs)
        self.note_content.set(**kwargs)


class NoteContent(BoxLayout):
    note_text = StringProperty()
    key_container = ObjectProperty()

    def __init__(self, **kwargs):
        if 'note_text' in kwargs:
            self.note_text = kwargs.pop('note_text')
        if 'kbd_buttons' in kwargs:
            self.key_container.keyboard_buttons = kwargs.pop('kbd_buttons')
        super().__init__(**kwargs)

    def set(self, **kwargs):
        if 'note_text' in kwargs:
            self.note_text = kwargs.pop("note_text")
        if 'kbd_buttons' in kwargs:
            self.key_container.keyboard_buttons = kwargs.pop('kbd_buttons')


class NoteTitle(BoxLayout):
    title_text = StringProperty()

    def __init__(self, **kwargs):
        if 'note_title' in kwargs:
            self.title_text = kwargs.pop('note_title')
        super().__init__(**kwargs)

    def set(self, **kwargs):
        if 'note_title' in kwargs:
            self.title_text = kwargs.pop('note_title')


class NoteContentKeyboard(BoxLayout):
    keyboard_buttons = ListProperty()

    def on_keyboard_buttons(self, *args, **kwargs):
        self.clear_widgets()
        n_btns = len(self.keyboard_buttons)
        last_btn = n_btns - 1

        # Multiple Keyboard buttons should take up 25% of horizontal Space
        # Single buttons should take up 10% of horizontal space
        # Inner spacing is n_buttons - 1

        if n_btns == 1:
            self.add_widget(KeyboardLabelSeparatorOuter(size_hint=(0.45, 1)))
            self.add_widget(KeyboardImage(text=self.keyboard_buttons[0], size_hint=(0.1, 1)))
            self.add_widget(KeyboardLabelSeparatorOuter(size_hint=(0.45, 1)))
        else:
            btn_size_hint_x = 0.25 / (n_btns + (n_btns - 1))
            for i, btn in enumerate(self.keyboard_buttons):
                if i == 0:
                    self.add_widget(KeyboardLabelSeparatorOuter(size_hint=(0.375, 1)))
                if n_btns >= i > 0:
                    self.add_widget(KeyboardLabelSeparatorInner(size_hint=(btn_size_hint_x, 1)))
                self.add_widget(KeyboardImage(text=btn))
                if i == last_btn:
                    self.add_widget(KeyboardLabelSeparatorOuter(size_hint=(0.375, 1)))


class NoteTags(BoxLayout):
    pass