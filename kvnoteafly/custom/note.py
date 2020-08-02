from functools import partial

from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from custom.keyboard import KeyboardLabelSeparatorOuter, KeyboardLabelSeparatorInner, KeyboardImage
from db import NoteType


class Note(BoxLayout):
    note_title = ObjectProperty()
    note_content = ObjectProperty()
    note_tags = ObjectProperty()

    def set_note_content(self, note_data: dict):
        title_data = {
            "title": note_data['title']
            }

        content_data = {
            "text":      note_data['text'],
            "keys_str":  note_data['keys_str'],
            "note_type": note_data['note_type']
            }

        self.note_title.set(title_data)
        self.note_content.set(content_data)


class NoteContent(BoxLayout):

    def set(self, content_data: dict):

        self.clear_widgets()

        if content_data['note_type'] == NoteType.TEXT_NOTE.name:
            self._set_text(content_data)
        elif content_data['note_type'] == NoteType.KEYBOARD_NOTE.name:
            self._set_keyboard(content_data)
        elif content_data['note_type'] == NoteType.RST_NOTE.name:
            self._set_rst(content_data)

    def _set_text(self, content_data: dict):
        pass

    def _set_keyboard(self, content_data: dict):
        self.add_widget(
                ContentKeyboard(content_data=content_data)
                )

    def _set_rst(self, content_data: dict):
        pass


class NoteTitle(BoxLayout):
    title_text = StringProperty()

    def __init__(self, **kwargs):
        if 'note_title' in kwargs:
            self.title_text = kwargs.pop('note_title')
        super().__init__(**kwargs)

    def set(self, title_data):
        self.title_text = title_data['title']


class ContentText(BoxLayout):
    pass


class ContentKeyboard(BoxLayout):
    note_text = StringProperty()
    keyboard_buttons = ListProperty()
    keyboard_animated_widgets = ListProperty()
    key_container = ObjectProperty()

    HSPACE_MULTI = 0.5
    HSPACE_MULTI_INNER_SEP = 0.2
    HSPACE_SINGLE = 0.2
    ANIMATION_WINDOW = 2

    def __init__(self, content_data, **kwargs):
        self.note_text = content_data['text']
        self.keyboard_buttons = content_data['keys_str'].split(",")
        super(ContentKeyboard, self).__init__(**kwargs)
        self.on_keyboard_buttons()

    @staticmethod
    def _set_btn_pressed(btn, *args):
        btn.pressed = True

    def _schedule_animations(self, *args, **kwargs):
        animation_interval = self.ANIMATION_WINDOW / len(self.keyboard_animated_widgets)

        for i, btn in enumerate(self.keyboard_animated_widgets, start=1):
            func = partial(self._set_btn_pressed, btn)
            Clock.schedule_once(func, (animation_interval * i))

    def on_keyboard_buttons(self, *args, **kwargs):
        self.key_container.clear_widgets()
        n_btns = len(self.keyboard_buttons)
        last_btn = n_btns - 1

        # Multiple Keyboard buttons should take up 50% of horizontal Space
        # Inner spacers take 20% of 50%
        # Single buttons should take up 50% of horizontal space
        # Inner spacing is n_buttons - 1

        if n_btns == 1:
            outer_sep_size = (1 - self.HSPACE_SINGLE) / 2

            self.key_container.add_widget(KeyboardLabelSeparatorOuter(size_hint=(outer_sep_size, 1)))
            kb_img = KeyboardImage(text=self.keyboard_buttons[0], size_hint=(self.HSPACE_SINGLE, 1))
            self.keyboard_animated_widgets.append(kb_img.proxy_ref)
            self.key_container.add_widget(kb_img)
            self.key_container.add_widget(KeyboardLabelSeparatorOuter(size_hint=(outer_sep_size, 1)))
        else:
            outer_sep_size = (1 - self.HSPACE_MULTI) / 2
            inner_size = (1 - self.HSPACE_MULTI)
            inner_sep_size = (inner_size * self.HSPACE_MULTI_INNER_SEP) / (n_btns - 1)
            inner_size_img = (inner_size - inner_sep_size) / n_btns

            for i, btn in enumerate(self.keyboard_buttons):
                if i == 0:
                    self.key_container.add_widget(KeyboardLabelSeparatorOuter(size_hint=(outer_sep_size, 1)))
                if n_btns >= i > 0:
                    self.key_container.add_widget(KeyboardLabelSeparatorInner(size_hint=(inner_sep_size, 1)))
                kb_img = KeyboardImage(text=btn, size_hint=(inner_size_img, 1))
                self.keyboard_animated_widgets.append(kb_img.proxy_ref)
                self.key_container.add_widget(kb_img)
                if i == last_btn:
                    self.key_container.add_widget(KeyboardLabelSeparatorOuter(size_hint=(outer_sep_size, 1)))

        Clock.schedule_once(self._schedule_animations, 0)


class ContentRST(BoxLayout):
    pass


class NoteTags(BoxLayout):
    pass
