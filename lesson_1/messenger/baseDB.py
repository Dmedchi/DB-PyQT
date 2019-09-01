# БД
# Декларативное создание таблицы 'Client', 'ClientContacts'
# Декларативное создание одноименных классов и их отображения

import os
from sqlalchemy import create_engine, Table, Column, Integer, String, Date, MetaData, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ---------------- Функция declarative_base создаёт базовый класс для декларативной работы -----------------------------

Base = declarative_base()


# ---------------------- На основании базового класса создаем необходимые классы ---------------------------------------


class Client(Base):
    """создает таблицу 'Client' и ее настраивает ее отображение"""
    __tablename__ = 'Client'  # название таблицы
    ClientId = Column(Integer, primary_key=True)  # Первичный ключ
    name = Column(String(25), unique=True)  # Имя пользователя
    info = Column(String, nullable=True)  # Информация (не обязательное поле)

    def __init__(self, name, info=None):
        self.name = name
        if info:
            self.info = info

    def __repr__(self):
        return "<Client('%s')>" % self.name

    def __eq__(self, other):
        return self.name == other.name  # Клиенты равны, если их имена равны


class ClientContacts(Base):
    """создает таблицу 'ClientContacts' и ее настраивает ее отображение"""
    __tablename__ = 'ClientContacts'
    ClientContactsId = Column(Integer, primary_key=True)
    ClientId = Column(Integer, ForeignKey('Client.ClientId'))  # id клиента
    ContactId = Column(Integer, ForeignKey('Client.ClientId'))  # id контакта клиента

    def __init__(self, client_id, contact_id):
        self.ClientId = client_id
        self.ContactId = contact_id

    def __repr__(self):
        return 'client_id = {} - friend_id = {}'.format(self.ClientId, self.ContactId)


# ------------------------------------- Settings -----------------------------------------------------------------------
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

# Рекомендуется брать 1 сессию и передавать параметром куда нам надо
# session = session

# Метеданные доступны через класс Base
metadata = Base.metadata

# ----------------------------------------------------------------------------------------------------------------------
# Таблица доступна через атрибут класса
# print(Client.__table__)
# print(ClientStory.__table__)
# print(ClientContacts.__table__)
