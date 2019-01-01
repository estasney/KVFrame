from kivy.uix.accordion import AccordionItem
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kvframe.buttons import *
import os
from kivy.lang import Builder
from kivy.app import App
from .scraper import NomadDriver

Builder.load_file('scraper/scraper_app.kv')


class ScraperView(AccordionItem):

    TITLE = "Scraper"
    scraper_status = StringProperty('Offline')

    scraper = None

    button1 = ObjectProperty()
    button2 = ObjectProperty()

    def on_scraper_status(self, *args, **kwargs):
        App.get_running_app().app_update(scraper_status=self.scraper_status)
        App.get_running_app().app_update(scraper=self.scraper)

    def launch(self):
        print("Launching")
        self.scraper = NomadDriver(service_path=os.path.realpath("scraper/chromedriver"))
        self.button1.disabled = True
        self.button2.disabled = False
        self.scraper_status = 'Online'

    def shutdown(self):
        print("Shutting down")

        self.scraper.shutdown()
        self.scraper = None
        self.button1.disabled = False
        self.button2.disabled = True
        self.scraper_status = 'Offline'

class SelectorView(AccordionItem):

    TITLE = "Selector"

    def get_scraper(self):
        return App.get_running_app().scraper

    def preview(self, *args, **kwargs):
        scraper = self.get_scraper()
        results = scraper.find_element("xpath", "//a")
        print(results)

    def select(self):
        print("select")















