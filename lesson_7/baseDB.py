"""БД: декларативное создание таблиц, одноименных классов и их отображения."""

import os
from sqlalchemy import create_engine, Table, Column, Integer, String, Date, MetaData, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Client(Base):
    __tablename__ = 'Client'
    ClientId = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True)
    info = Column(String, nullable=True)

    def __init__(self, name, info=None):
        self.name = name
        if info:
            self.info = info

    def __repr__(self):
        return "<Client('%s')>" % self.name

    def __eq__(self, other):
        return self.name == other.name


class ClientContacts(Base):
    __tablename__ = 'ClientContacts'
    ClientContactsId = Column(Integer, primary_key=True)
    ClientId = Column(Integer, ForeignKey('Client.ClientId'))
    ContactId = Column(Integer, ForeignKey('Client.ClientId'))

    def __init__(self, client_id, contact_id):
        self.ClientId = client_id
        self.ContactId = contact_id

    def __repr__(self):
        return 'client_id = {} - friend_id = {}'.format(self.ClientId, self.ContactId)


# путь до папки, где лежит этот модуль
DB_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

# путь до файла базы данных
DB_PATH = os.path.join(DB_FOLDER_PATH, 'Server.db')

# создать движок
engine = create_engine('sqlite:///{}'.format(DB_PATH), echo=False)

# Выполнить запрос (CREATE TABLE) на создание таблицы
Base.metadata.create_all(engine)

# Создать сессию для работы
Session = sessionmaker(bind=engine)

# Создать Session-объект, который привязан к базе данных
session = Session()

metadata = Base.metadata
