import os
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import NumericProperty

from kvtopic.backend import DocumentIndex
from kvtopic.buttons import *
from kvtopic.custom import *

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
z = RedRoundedButton  # prevents pycharm
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

    screen_manager = ObjectProperty()

    clock_time = StringProperty()
    resource_dir = StringProperty()
    n_docs = NumericProperty()
    n_topics = NumericProperty()
    n_topic_names = NumericProperty()  # This is derived from topic_names
    job_families = ListProperty()
    job_titles = ListProperty()
    topic_names = ListProperty()

    # document
    current_document_title = StringProperty()
    current_document_topics = StringProperty()
    current_document_text = StringProperty()

    def on_topic_names(self, *args, **kwargs):
        self.n_topic_names = len(self.topic_names)

    def get_time(self, *args, **kwargs):
        self.clock_time = datetime.strftime(datetime.now(), "%I:%M:%S %p")

    def update_available(self, value, col):

        self.DATA_INDEX.filter_by(value, col)
        Clock.schedule_once(self.refresh_filter_status_properties)

    def refresh_filter_status_properties(self, *args, **kwargs):
        self.job_families = []
        self.job_families = sorted(self.DATA_INDEX.job_families)
        self.topic_names = []
        self.topic_names = self.DATA_INDEX.topic_names
        self.job_titles = []
        self.job_titles = sorted(self.DATA_INDEX.job_titles)
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
        callback = kwargs.get('callback', None)
        callback_kwargs = kwargs.get('callback_kwargs', {})

        self.DATA_INDEX.reset_filters()

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
        if idx_filters:
            self.DATA_INDEX.apply_filters(idx_filters)
            Clock.schedule_once(self.refresh_filter_status_properties)
        if callback:
            callback(**callback_kwargs)




    def setup_backend(self, *args, **kwargs):
        self.n_docs = self.DATA_INDEX.n_docs_resulting
        self.n_topics = self.DATA_INDEX.n_topics_resulting
        self.job_titles = sorted(self.DATA_INDEX.job_titles)
        self.job_families = sorted(self.DATA_INDEX.job_families)
        self.topic_names = sorted(self.DATA_INDEX.topic_names)
        self.n_topic_names = len(self.topic_names)

    def values_filter(self, *args, **kwargs):
        value, caller_id = kwargs.pop('value'), kwargs.pop('input_id')

        # Callers input_job_family, input_job_title, input_topic_name

        # Is this widget being returned to default state?
        if isinstance(value, str) and value.startswith("All "):
            return

        if caller_id == "input_job_family":
            self.update_available(value, col="Job_Family")
        elif caller_id == "input_job_title":
            self.update_available(value, "Job_Title")
        elif caller_id == "input_topic_name":
            # 1:1+ name: ids
            value = self.DATA_INDEX.topic_data.name2id[value]
            self.update_available(value, col="T1")

    def show_documents(self, *args, **kwargs):
        self.screen_manager.current = 'documents'

    def build(self):
        self.get_time()
        self.setup_backend()
        sm = ScreenManagement()
        self.screen_manager = sm
        Clock.schedule_interval(self.get_time, 0.1)
        return sm


if __name__ == "__main__":
    TopicApp().run()
