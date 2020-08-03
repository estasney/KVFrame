from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout

from utils import import_kv

import_kv(__file__)


class NoteCategoryChooser(StackLayout):
    manager = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def category_callback(self, instance):
        self.manager.category_selected(instance)

    def set_categories(self, categories):
        category_widgets = [Button(text=cat, size_hint=(0.25, 0.25)) for cat in categories]
        for cat in category_widgets:
            cat.bind(on_release=self.category_callback)
            self.add_widget(cat)


class NoteCategoryButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
