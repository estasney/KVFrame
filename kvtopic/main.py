import os
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import NumericProperty, ListProperty

from kvtopic.backend import DocumentIndex
from kvtopic.buttons import *
from kvtopic.custom import *

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
z = RedButton  # prevents pycharm
z = ScreenManagement


class TopicApp(App):
    APP_NAME = "KVTopic"
    APP_VERSION_ = 1
    APP_VERSION = "v{}".format(APP_VERSION_)
    APP_ICON_PATH = os.path.realpath("resources/logo.png")
    TOPICS_PATH = os.path.realpath("resources/topics/topics.pkl")
    DOCS_PATH = os.path.realpath("resources/docs/docs.pkl")
    GREEN_TEXT = "#21fc0d"
    RED_TEXT = "#fe420f"
    DATA_INDEX = DocumentIndex(DOCS_PATH, TOPICS_PATH)

    clock_time = StringProperty()
    resource_dir = StringProperty()
    n_docs = NumericProperty()
    n_topics = NumericProperty()
    job_families = ListProperty()
    job_titles = ListProperty()
    topic_names = ListProperty()

    def get_time(self, *args, **kwargs):
        self.clock_time = datetime.strftime(datetime.now(), "%I:%M:%S %p")

    def update_available(self, value, col):
        self.DATA_INDEX.filter_by(value, col)
        Clock.schedule_once(self.refresh_filter_status_properties)

    def refresh_filter_status_properties(self, *args, **kwargs):
        self.job_families = []
        self.job_families = self.DATA_INDEX.job_families
        self.topic_names = []
        self.topic_names = self.DATA_INDEX.topic_names
        self.job_titles = []
        self.job_titles = self.DATA_INDEX.job_titles
        self.n_docs = 0
        self.n_docs = self.DATA_INDEX.n_docs_resulting
        self.n_topics = 0
        self.n_topics = self.DATA_INDEX.n_topics_resulting

    def set_filters(self, *args, **kwargs):
        if 'reset' in kwargs:
            self.DATA_INDEX.reset_filters()
            Clock.schedule_once(self.refresh_filter_status_properties)
            return
        job_family = kwargs.pop('job_family')
        job_title = kwargs.pop('job_title')
        topic_name = kwargs.pop('topic')
        word_search = kwargs.pop('word_search')
        word_boolean_is_all = kwargs.pop('word_boolean')

        idx_filters = []  # Will reduce at the end
        if job_family[:4] != "All ":
            idx_filters.append(self.DATA_INDEX.filter_by(job_family, col="Job_Family", set_idx=False))
        if job_title[:4] != "All ":
            idx_filters.append(self.DATA_INDEX.filter_by(job_title, col="Job_Title", set_idx=False))
        if topic_name[:4] != "All ":
            topic_ids = self.DATA_INDEX.topic_data.name2id[topic_name]
            idx_filters.append(self.DATA_INDEX.filter_by(topic_ids, col="T1", set_idx=False))
        if word_search != "":
            words = word_search.split(",")
            words = [x.strip() for x in words]
            print(words)
            if word_boolean_is_all:
                f = self.DATA_INDEX.having_all_words
            else:
                f = self.DATA_INDEX.having_any_words
            idx_filters.append(f(words=words, col="Job_Description", set_idx=False))
        if not idx_filters:
            return
        self.DATA_INDEX.apply_filters(idx_filters)
        Clock.schedule_once(self.refresh_filter_status_properties)

    def setup_backend(self, *args, **kwargs):
        self.n_docs = self.DATA_INDEX.n_docs_resulting
        self.n_topics = self.DATA_INDEX.n_topics_resulting
        self.job_titles = self.DATA_INDEX.job_titles
        self.job_families = self.DATA_INDEX.job_families
        self.topic_names = self.DATA_INDEX.topic_data.topic_names

    def values_filter(self, *args, **kwargs):
        value, col = kwargs.pop('value'), kwargs.pop('col')
        self.update_available(value, col)

    def build(self):
        self.get_time()
        self.setup_backend()
        Clock.schedule_interval(self.get_time, 0.1)


if __name__ == "__main__":
    TopicApp().run()
