from typing import List

from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from utils import import_kv

import_kv(__file__)


class ScrollingListView(ScrollView):
    child_object = ObjectProperty()

    def set(self, items: List[dict], *args, **kwargs):
        if not self.children:
            layout = ListView(cols=1, size_hint=(None, None), width=Window.width)
            layout.bind(minimum_height=layout.setter('height'))
            self.add_widget(layout)
            self.child_object = layout
        self.children[0].set(items)


class ListItem(GridLayout):
    title_text = StringProperty()
    index = NumericProperty()

    def __init__(self, content_data: dict, *args, **kwargs):
        self.title_text = content_data['title']
        self.index = content_data['idx']
        super().__init__(**kwargs)


class ListView(GridLayout):

    def set(self, notes: List[dict]):
        self.clear_widgets()
        for note in notes:
            self.add_widget(
                    ListItem(content_data=note, width=Window.width, height=(Window.height / 6),
                             size_hint=(None, None))
                    )
