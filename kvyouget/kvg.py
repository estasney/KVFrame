import os
import sys
import threading
from functools import partial

from dotenv import load_dotenv
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.properties import (OptionProperty, ObjectProperty, ListProperty, StringProperty, DictProperty,
                             NumericProperty)

from kvyouget.custom.screens import KVGScreenManager
from kvyouget.dl.utils import get_url_options, Result


class KVG(App):
    """
    Attributes
    ----------


    """

    APP_NAME = 'KVG'
    screen_manager = ObjectProperty()

    itags = ListProperty()
    url_title = StringProperty()

    colors = DictProperty({
        "Light":   (0.3843137254901961, 0.4470588235294118, 0.4823529411764706),
        "Primary": (0.21568627450980393, 0.2784313725490195, 0.30980392156862746),
        "Dark":    (0.06274509803921569, 0.1254901960784313, 0.15294117647058825),
        "Accent1": (0.8588235294117648, 0.227450980392157, 0.20392156862745092),
        "Accent2": (0.02352941176470591, 0.8392156862745098, 0.6274509803921572)
        })

    def run_threaded(self, target_function, *args, **kwargs):
        threading.Thread(target=target_function, args=args, kwargs=kwargs).start()

    def download_action(self, action, value):
        print(action)
        print(value)
        self.run_threaded(self.get_itags, url=value)

    def set_screen(self, *args, **kwargs):

        self.screen_manager.current = args[0]

    def build(self):
        sm = KVGScreenManager(self)
        self.screen_manager = sm
        return sm

    def get_itags(self, url):
        # Animate the screen change
        f1 = partial(self.set_screen, "chooser_screen")
        Clock.schedule_once(f1, 0)

        # Blocking Operation
        results = get_url_options(url)
        self.update_url_options(results)

    @mainthread
    def update_url_options(self, result: Result):
        print(result.itags)
        self.itags = result.itags
        self.url_title = result.title


if __name__ == '__main__':
    sys.path.append(os.getcwd())
    load_dotenv()
    KVG().run()
