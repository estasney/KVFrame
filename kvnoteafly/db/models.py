import os
from datetime import datetime
from enum import Enum, IntEnum
from pathlib import Path
from typing import Optional, List

from sqlalchemy import Column, Integer, create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()

basedir = os.path.abspath(os.path.dirname(__file__))

db_path = f"sqlite:///{Path(basedir).as_posix()}/noteafly.db"


def create_session(db_path=db_path, base=Base):
    engine = create_engine(db_path)
    if not database_exists(engine.url):
        create_database(engine.url)
    base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


class DictMixin:

    def to_dict(self, recurse_relations: Optional[List[Base]] = None, **kwargs) -> dict:
        """
        Convert values to dict
        Returns
        -------

        """

        def handle_enums(x):
            if not isinstance(x, Enum):
                return x
            return x.name

        def handle_nested_list(x: InstrumentedList):
            output = []
            for item in x:
                if hasattr(item, 'to_dict'):
                    item: DictMixin
                    if recurse_relations is not None and item.__class__ in recurse_relations:
                        output.append(item.to_dict(recurse_relations=recurse_relations))
                else:
                    output.append(str(item))
            return output

        def route_type(x):
            if isinstance(x, Enum):
                return handle_enums
            elif hasattr(x, 'to_dict'):
                return getattr(x, 'to_dict')
            elif isinstance(x, datetime):
                return lambda y: getattr(y, 'isoformat')()
            elif isinstance(x, InstrumentedList):
                return handle_nested_list
            else:
                return lambda y: y

        def handle(x):
            f = route_type(x)
            return f(x)

        raw_data = {k: v for k, v in vars(self).items()}
        properties = [k for k, v in vars(self.__class__).items() if isinstance(v, property)]
        data = {k: handle(v) for k, v in raw_data.items() if self._filter_key(k)}
        for k in properties:
            if self._filter_key(k):
                data[k] = handle(getattr(self, k))
        return data

    def _filter_key(self, k: str) -> bool:
        if k.startswith("_"):
            return False
        return True


class NoteType(IntEnum):
    TEXT_NOTE = 0
    KEYBOARD_NOTE = 1
    CODE_NOTE = 2

class NoteCategory(IntEnum):
    Windows = 0
    Python = 1
    Chrome = 2
    SQLAlchemy = 3
    PyCharm = 4
    Jinja = 5
    Pandas = 6
    Git = 7
    Regex = 8
    CSS = 9
    Rst = 10
    Excel = 11
    Docker = 12
    Bash = 13


class Note(Base, DictMixin):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    keys_str = Column(String(128))
    text = Column(String(1024))
    _category = Column(Integer, default=0)
    _note_type = Column(Integer, default=0)

    @property
    def keys(self):
        return self.keys_str

    @keys.getter
    def keys(self):
        if self.keys_str:
            return self.keys_str.split(",")
        else:
            return None

    @keys.setter
    def keys(self, kbd_keys: List[str]):
        self.keys_str = ",".join(kbd_keys)

    @property
    def note_type(self) -> int:
        return self._note_type

    @note_type.getter
    def note_type(self):
        return NoteType(self._note_type)

    @note_type.setter
    def note_type(self, nt: NoteType):
        self._note_type = nt.value

    @property
    def category(self) -> int:
        return self._category

    @category.getter
    def category(self):
        return NoteCategory(self._category)

    @category.setter
    def category(self, category: NoteCategory):
        self._category = category.value
