import os
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import NumericProperty, BooleanProperty
from kivy.graphics import Rectangle
from kivy.graphics import Color as KivyColor
from unicodedata import normalize


from kvtopic.backend import DocumentIndex
from kvtopic.buttons import *
from kvtopic.custom import *
from kvtopic.keyword_highlighter import generate_highlighter_colors, ColoredKeywordProcessor

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'default_font', ['CiscoSansTT'])
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
    doc_label = ObjectProperty()

    clock_time = StringProperty()
    resource_dir = StringProperty()
    n_docs = NumericProperty()
    n_topics = NumericProperty()
    n_topic_names = NumericProperty()  # This is derived from topic_names
    job_families = ListProperty()
    job_titles = ListProperty()
    topic_names = ListProperty()

    doc_highlighter_data = {}  # Color : keywords
    color_dict = {}

    # document
    current_document_title = StringProperty()
    current_document_topics = StringProperty()
    current_document_text = StringProperty()
    current_document_idx = NumericProperty()
    current_document_idx_max = NumericProperty()
    current_document_idx_str = StringProperty()
    current_document_next_enabled = BooleanProperty(False)
    current_document_previous_enabled = BooleanProperty(False)

    @staticmethod
    def get_x(label, ref_x):
        """ Return the x value of the ref/anchor relative to the canvas """
        return label.center_x - label.texture_size[0] * 0.5 + ref_x

    @staticmethod
    def get_y(label, ref_y):
        """ Return the y value of the ref/anchor relative to the canvas """
        # Note the inversion of direction, as y values start at the top of
        # the texture and increase downwards
        return label.center_y + label.texture_size[1] * 0.5 - ref_y



    def on_topic_names(self, *args, **kwargs):
        self.n_topic_names = len(self.topic_names)

    def on_current_document_idx(self, *args, **kwargs):
        self.current_document_idx_str = "{} of {}".format((self.current_document_idx + 1),
                                                          self.current_document_idx_max)
        if self.current_document_previous_enabled is False:
            if self.current_document_idx > 0:
                self.current_document_previous_enabled = True
        else:
            if self.current_document_idx == 0:
                self.current_document_previous_enabled = False

        if self.current_document_next_enabled is False:
            if (self.current_document_idx + 1) < self.current_document_idx_max:
                self.current_document_next_enabled = True
        else:
            if (self.current_document_idx + 1) >= self.current_document_idx_max:
                self.current_document_next_enabled = False

    def on_current_document_idx_max(self, *args, **kwargs):
        self.on_current_document_idx()

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

    def setup_highlighter_data(self):
        """
        Create ColoredKeywordProcessor and populate with colors and their keywords
        """
        kws = {}
        for i, name in enumerate(self.topic_names):
            topic_kws = self.DATA_INDEX.name2keywords[name]
            kws[name] = {'keywords': topic_kws}
        self.doc_highlighter_data = kws

    def setup_backend(self, *args, **kwargs):
        self.n_docs = self.DATA_INDEX.n_docs_resulting
        self.n_topics = self.DATA_INDEX.n_topics_resulting
        self.job_titles = sorted(self.DATA_INDEX.job_titles)
        self.job_families = sorted(self.DATA_INDEX.job_families)
        self.topic_names = sorted(self.DATA_INDEX.topic_names)
        self.n_topic_names = len(self.topic_names)
        self.setup_highlighter_data()

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

    def format_topic_header(self, doc_dict):
        # get topic Ids and their scores
        topic_score_cols = zip(["T1", "T2", "T3"], ["S1", "S2", "S3"])
        topic_data_header = []
        color_list = generate_highlighter_colors(n_colors=3)
        color_dict = {}
        for i, (topic_id_col, topic_score_col) in enumerate(topic_score_cols):
            topic_id, topic_score = doc_dict[topic_id_col], round(doc_dict[topic_score_col], 2)
            topic_name = self.DATA_INDEX.topic_data.id2name[topic_id]
            topic_color = color_list[i]
            color_dict[topic_name] = topic_color
            topic_str = "[color={color}]{topic_name}[/color]: {score}".format(color=topic_color, topic_name=topic_name,
                                                                              score=topic_score)
            topic_data_header.append(topic_str)
        self.color_dict = color_dict
        return ", ".join(topic_data_header)




    def cleanup_text(self, text):
        text = normalize("NFKD", text)
        text = text.encode().decode('ascii', errors='ignore')
        text = text.replace("\t", "    ")
        return text

    def format_doc_text(self, doc_dict):
        doc_text = doc_dict['Job_Description']
        doc_text = self.cleanup_text(doc_text)

        # what topics are we highlighting?
        topic_ids = [doc_dict[col] for col in ["T1", "T2", "T3"]]
        topics_names = [self.DATA_INDEX.topic_data.id2name[i] for i in topic_ids]
        topics_keywords = {}
        keywords_seen = set([])
        for name in topics_names:
            topic_kws_data = self.doc_highlighter_data[name]
            topic_color, topic_kws = self.color_dict[name], topic_kws_data['keywords']
            topic_kws = [word for word in topic_kws if word not in keywords_seen]
            keywords_seen.update(set(topic_kws))
            topics_keywords[topic_color] = topic_kws
        kp = ColoredKeywordProcessor()
        kp.add_colored_keywords(topics_keywords)
        formatted_text = kp.colorize_keywords(doc_text)
        return formatted_text

    def setup_document(self, *args, **kwargs):
        """Fetch and format documents screen. Content is supplied from self.DATA_INDEX. App handles formatting and display"""
        doc_dict = self.DATA_INDEX.current_doc
        doc_idx, group_len = self.DATA_INDEX.current_index
        self.current_document_title = doc_dict['Job_Title']
        self.current_document_topics = self.format_topic_header(doc_dict)
        self.current_document_text = self.format_doc_text(doc_dict)
        self.current_document_idx = doc_idx
        self.current_document_idx_max = group_len
        Clock.schedule_once(self.highlight_doc_label, 0.5)

    def highlight_doc_label(self, *argas, **kwargs):
        label = self.doc_label
        label.canvas.before.clear()

        for name, boxes in label.refs.items():
            color_name = name.split("_")[0]
            for box in boxes:
                with label.canvas.before:
                    c = get_color_from_hex(color_name)[:3]
                    c.append(0.7)
                    KivyColor(*c)
                    Rectangle(pos=(self.get_x(label, box[0]),
                                   self.get_y(label, box[1])),
                              size=(box[2] - box[0],
                                    box[1] - box[3]))


    def show_documents(self, *args, **kwargs):
        self.setup_document()
        self.screen_manager.current = 'documents'

    def paginate(self, kind: str, n: int):

        if kind == 'advance':
            self.DATA_INDEX.advance(n)
        else:
            self.DATA_INDEX.reverse(n)
        self.setup_document()

    def show_options(self):
        self.set_filters(reset=True)
        self.screen_manager.current = 'options'

    def build(self):
        self.get_time()
        self.setup_backend()
        sm = ScreenManagement()
        self.screen_manager = sm
        screens = self.screen_manager.screens
        documents_screen = next((x for x in screens if x.name == 'documents'), None)
        self.doc_label = documents_screen.ids['doc_text']
        Clock.schedule_interval(self.get_time, 0.1)
        return sm


if __name__ == "__main__":
    TopicApp().run()
