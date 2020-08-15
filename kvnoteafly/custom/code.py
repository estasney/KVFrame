from kivy.properties import StringProperty
from kivy.uix.anchorlayout import AnchorLayout

from utils import import_kv

import_kv(__file__)

class ContentCode(AnchorLayout):
    note_text = StringProperty()

    def __init__(self, content_data, **kwargs):
        self.note_text = content_data['text']
        super(ContentCode, self).__init__(**kwargs)
