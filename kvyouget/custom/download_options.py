from typing import List

from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from dl.utils import ITag, Result
from kvyouget.custom.scroller import ScrollingListView, ListView
from utils import import_kv

import_kv(__file__)


class DownloadOptions(ScrollingListView):
    child_object = ObjectProperty()

    def set(self, result: Result, *args, **kwargs):
        if not self.children:
            layout = ITagListView(cols=1, size_hint=(None, None), width=Window.width)
            layout.bind(minimum_height=layout.setter('height'))
            self.add_widget(layout)
            self.child_object = layout
        self.children[0].set(result)


class ITagListView(ListView):

    def set(self, result: Result):
        self.clear_widgets()
        self.add_widget(
                ITagTitleItem(title=result.title, width=Window.width, height=(Window.height / 6),
                              size_hint=(None, None))
                )
        for itag in result.itags:
            self.add_widget(
                    ITagListItem(itag=itag, width=Window.width, height=(Window.height / 6),
                                 size_hint=(None, None))
                    )


class ITagTitleItem(BoxLayout):
    title = StringProperty()

    def __init__(self, title, **kwargs):
        self.title = title
        super().__init__(**kwargs)


class ITagListItem(GridLayout):
    itag_id = StringProperty()
    container = StringProperty()
    quality = StringProperty()
    itag_size = StringProperty()
    itag_xy = StringProperty()

    def __init__(self, itag: ITag, **kwargs):
        self.itag_id = str(itag.itag)
        self.container = str(itag.container)
        self.quality = str(itag.quality)
        self.itag_size = itag.size_mb
        self.itag_xy = str(f"{itag.x} , {itag.y}")
        super().__init__(**kwargs)

    def select_itag(self, *args, **kwargs):
        print(f"Select ITag {self.itag_id}")
