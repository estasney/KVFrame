from typing import List

from kivy.core.window import Window
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout

from kvyouget.custom.scroller import ScrollingListView, ListView
from utils import import_kv

import_kv(__file__)

class DownloadOptionsContainer(BoxLayout):
    itags = ListProperty()
    pass


class DownloadOptions(ScrollingListView):
    child_object = ObjectProperty()

    def set(self, items: List[dict], *args, **kwargs):
        if not self.children:
            layout = ListView(cols=1, size_hint=(None, None), width=Window.width)
            layout.bind(minimum_height=layout.setter('height'))
            self.add_widget(layout)
            self.child_object = layout
        self.children[0].set(items)
