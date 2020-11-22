import os
import sys
import threading
from pathlib import Path

from dotenv import load_dotenv
from kivy.app import App
from kivy.clock import mainthread
from kivy.properties import (ObjectProperty, StringProperty, DictProperty)

from kvyouget.custom.screens import KVGScreenManager
from kvyouget.dl.utils import get_url_options, download_url


class KVG(App):
    """
    Attributes
    ----------


    """

    APP_NAME = 'KVG'
    screen_manager = ObjectProperty()
    url_title = StringProperty()
    url = StringProperty()
    status = StringProperty("Loading")

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
        self.url = value
        self.set_screen("loading_screen")
        self.run_threaded(self.get_itags, url=value)

    def set_screen(self, *args, **kwargs):
        self.screen_manager.current = args[0]

    def _on_download_complete(self, *args, **kwargs):
        self.download_complete()

    @mainthread
    def download_complete(self, *args, **kwargs):
        self.url = ""
        self.status = "Loading"
        self.set_screen("input_url_screen")

    def build(self):
        sm = KVGScreenManager(self)
        self.screen_manager = sm
        return sm

    def get_itags(self, url):
        # Blocking Operation
        result = get_url_options(url)
        self.screen_manager.handle_itag_result(result)

    def cancel_itag(self):
        self.url = ""
        self.set_screen("input_url_screen")

    def select_itag(self, value):
        self.status = f"Downloading ITag: {value}"
        self.set_screen("loading_screen")
        self.run_threaded(download_url, url=self.url, itag=int(value),
                          output_dir=str(os.path.join(Path.home(), "Downloads")),
                          on_complete=self._on_download_complete)


if __name__ == '__main__':
    sys.path.append(os.getcwd())
    load_dotenv()
    KVG().run()
