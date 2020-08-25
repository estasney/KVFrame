from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.vector import Vector
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
        category_widgets = [NoteCategoryButton(text=cat, size_hint=(0.25, 0.25)) for cat in value]
        for cat in category_widgets:
            cat.bind(on_release=self.category_callback)
            self.add_widget(cat)

class NoteCategoryButton(ButtonBehavior, BoxLayout):

    source = StringProperty()
    text = StringProperty()

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.source = f"atlas://static/category_icons/category-img/{text.lower()}"
        self.text = text

    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2


