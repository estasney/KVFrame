from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout

from utils import import_kv

import_kv(__file__)


class NoteCategoryChooser(StackLayout):
    manager = ObjectProperty()
    categories = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def category_callback(self, instance):
        self.manager.category_selected(instance)

    def on_categories(self, instance, value):
        category_widgets = [Button(text=cat, size_hint=(0.25, 0.25)) for cat in value]
        for cat in category_widgets:
            cat.bind(on_release=self.category_callback)
            self.add_widget(cat)


class NoteCategoryButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
