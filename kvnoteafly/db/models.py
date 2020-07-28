from sqlalchemy import Column, Integer, create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from collections import namedtuple

import os
from pathlib import Path

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

NoteTuple = namedtuple('NoteTuple', 'note_title note_text, kbd_buttons')


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    keys_str = Column(String(128))
    text = Column(String(1024))

    def to_tuple(self):
        return NoteTuple(note_title=self.title, note_text=self.text, kbd_buttons=self.keys)

    @property
    def keys(self):
        return self.keys_str

    @keys.getter
    def keys(self):
        return self.keys_str.split(",")

    @keys.setter
    def keys(self, kbd_keys):
        self.keys_str = ",".join(kbd_keys)
