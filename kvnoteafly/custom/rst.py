from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from utils import import_kv

import_kv(__file__)

class ContentRST(BoxLayout):
    note_text = StringProperty()

    def __init__(self, content_data, **kwargs):
        self.note_text = content_data['text']
        super(ContentRST, self).__init__(**kwargs)
