import pickle
import re
from typing import Union
import numpy as np
import pandas as pd


class TopicIndex(object):

    def __init__(self, fp):
        self.fp = fp
        self.data = self.load_fp(fp)
        self.topic_names = [v['name'] for v in list(self.data.values())]
        self.id2name = {}
        self.name2id = {}
        for k, v in self.data.items():  # k int key, v is {'name': x, 'words': []}
            topic_id, topic_name = k, v['name']
            matching_ids = self.name2id.get(topic_name, [])
            matching_ids.append(topic_id)
            self.name2id[topic_name] = matching_ids
            self.id2name[topic_id] = topic_name

    def __len__(self):
        return len(self.data)

    def load_fp(self, fp):
        with open(fp, "rb") as f:
            return pickle.load(f)


class DocumentIndex(object):

    def __init__(self, fp_data, fp_topics):
        self.fp_data = fp_data
        self.fp_topics = fp_topics
        self.data = pd.read_pickle(fp_data)
        self.idx_filter = None
        self.idx_counter = 0
        self.topic_data = TopicIndex(fp_topics)

    @property
    def topic_names(self):
        if self.idx_filter is None:
            return self.topic_data.topic_names

        d = self.data.loc[self.idx_filter]
        topic_numbers = d.T1.unique().tolist()
        return [self.topic_data.id2name[x] for x in topic_numbers]

    @property
    def n_docs(self):
        return len(self.data)

    @property
    def n_docs_resulting(self):
        if self.idx_filter is None:
            return self.n_docs
        else:
            return len(self.data.loc[self.idx_filter])

    @property
    def n_topics(self):
        return len(self.topic_data)

    @property
    def n_topics_resulting(self):
        if self.idx_filter is None:
            return self.n_topics
        else:
            filtered_data = self.data.loc[self.idx_filter]
            available_topics = filtered_data['T1'].unique().tolist()
            return len(available_topics)

    @property
    def job_titles(self):
        unique_titles = self.list_unique('Job_Title')
        unique_titles = [x for x in unique_titles if isinstance(x, str) and x != ""]
        return unique_titles

    @property
    def job_families(self):
        unique_families = self.list_unique('Job_Family')
        unique_families = [x for x in unique_families if isinstance(x, str) and x != ""]
        return unique_families


    @property
    def results(self):
        if self.idx_filter is not None:
            return self.data.loc[self.idx_filter]
        else:
            return self.data

    def _compute_unique(self, col):
        if self.idx_filter is None:
            filtered_data = self.data
        else:
            filtered_data = self.data.loc[self.idx_filter]

        unique_values = filtered_data[col].unique()
        return unique_values


    def count_unique(self, col):
        unique_values = self._compute_unique(col).tolist()
        return len(unique_values)

    def list_unique(self, col):
        unique_values = self._compute_unique(col).tolist()
        return unique_values


    def next_match(self):
        filtered_data = self.results
        next_match = filtered_data.iloc[self.idx_counter].to_dict()
        self.idx_counter += 1
        return next_match

    def reset_filters(self):
        self.idx_filter = None
        self.idx_counter = 0

    def apply_filters(self, filters: list):
        flat_filters = np.logical_and.reduce(filters)
        self.idx_filter = flat_filters

    def filter_by(self, search: Union[str, int, float, list], col: str, set_idx=True) -> np.ndarray:
        if isinstance(search, list):
            result = self._filter_bys(search, col)
        else:
            result = self._filter_by(search, col)
        if set_idx:
            self.idx_filter = result
        return result

    def _filter_by(self, search, col: str) -> np.ndarray:
        return (self.data[col] == search).values

    def _filter_bys(self, search:list, col:str) -> np.ndarray:
        filters = [self.data[col]==item for item in search]
        return np.logical_or.reduce(filters)

    def _word_search(self, words: list, col='Job_Description'):
        f = [self.data[col].str.contains(r"\s?{}\s".format(w), regex=True, flags=re.IGNORECASE) for w in words]
        return f

    def having_all_words(self, words: list, col="Job_Description", set_idx=True):
        result = self._having_all_words(words, col)
        if set_idx:
            self.idx_filter = result
        return result

    def _having_all_words(self, words: list, col='Job_Description'):
        f = self._word_search(words, col)
        return np.logical_and.reduce(f)

    def having_any_words(self, words: list, col="Job_Description", set_idx=True):
        result = self._having_any_words(words, col)
        if set_idx:
            self.idx_filter = result
        return result

    def _having_any_words(self, words: list, col='Job_Description'):
        f = self._word_search(words, col)
        return np.logical_or.reduce(f)
