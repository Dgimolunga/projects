# -*- coding: utf-8 -*-
# import sqlite3
#
#
# db_connect = sqlite3.connect("script_db.db")
# cursor = db_connect.cursor()
#
# list_ = []
# for i in range(3):
#     list_.append((i, '79525368325', 234342, 'asdfasf', 'session_id_{}'.format(i), str(False)))
# cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?,?)", list_)
# sql_select = """
# select * from users
# where id=?
# """
# cursor.execute(sql_select, [1])
# print(cursor.fetchall())
# input("sdf:? ")
# db_connect.commit()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.session import sessionmaker

import re

# from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///USERBOT_DB.db', echo=True)
Base = declarative_base(engine)
session_db = sessionmaker(bind=engine)()


class NotCorrect(Exception):
    pass


class DataDuplicateExc(Exception):
    pass

arg_user_db = [
    'telegram_id',
    'phone',
    'api_id',
    'api_hash',
    'share_channel_id',
    'start_script'
]
__arg_user_db = [
    'telegram_id',
    'phone',
    'api_id',
    'api_hash',
    'share_channel_id',
    'session_name',
    'state',
    'start_script'
]
arg_for_session = [
    'phone',
    'api_id',
    'api_hash',
    'share_channel_id'
]

arg_other = [
    "some arg...."
]

command_set_list = [
    'phone',
    'api_id',
    'api_hash',
    'share_channel_id',
]

command_get_list = [
    'phone',
    'api_id',
    'api_hash',
    'share_channel_id',
]


def raise_exc(error):
    raise NotCorrect(error)


def phone_check(phone):
    return phone


def re_check(data, res, error_msg):
    re_data = re.findall(res, data)
    if not (''.join(re_data) == data):
        raise_exc(error_msg)
    return data


# def int_check(data):
#     re_data = re.findall(r'^[0-9]+', data)
#     if not (''.join(re_data) == data):
#         rais_exc("Значение должно состоять из цыфр")
#     return data
#
# def hash_check(data):
#     re_hash = re.findall(r'^[a-zA-Z0-9]+', api_hash)
#     print(re_hash)
#     if not (''.join(re_hash) == api_hash):
#         pass


check_arg_dict = {
    'telegram_id': lambda t_id: raise_exc('telegram not integer') if type(t_id) == type(1) else t_id,
    'phone': lambda phone: phone_check(phone),
    'api_id': lambda api_id: re_check(api_id, r'^[0-9]+', "Неверный формат api_id (от должен состоять из цыфр)"),
    'api_hash': lambda api_hash: re_check(api_hash, r'^[a-zA-Z0-9]+', 'Неверный формат api_hash'),
    'share_channel_id': lambda share_channel_id: re_check(share_channel_id, r'^[0-9]+',
                                                          "Неверный формат share_channel_id (от должен состоять из цыфр)")

}


class User(Base):
    __tablename__ = 'UserBots'
    key_userbot = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)  # а если кто то захочет зарегать
    phone = Column(String)
    api_id = Column(Integer)
    api_hash = Column(String)
    session_name = Column(String)
    state = Column(String)
    start_script = Column(String)


class Ticker(Base):
    __tablename__ = 'Tickers'
    key_ticker = Column(Integer, primary_key=True)
    key_userbot = Column(Integer)
    ticker = Column(String)


class Tag(Base):
    __tablename__ = 'Tags'
    key_tag = Column(Integer, primary_key=True)
    key_userbot = Column(Integer)
    key_ticker = Column(Integer)
    tag = Column(String)


class ShareChannel(Base):
    __tablename__ = 'ShareChannels'
    key_sharechannel = Column(Integer, primary_key=True)
    key_userbot = Column(Integer)
    share_channel_id = Column(Integer)


class ParsChannel(Base):
    __tablename__ = 'ParsChannels'
    key_parschannel = Column(Integer, primary_key=True)
    key_userbot = Column(Integer)
    pars_channel_id = Column(Integer)

    # def __repr__(self):
    #     return '<User(telegram_id="{}", phone="{}", api_id="{}", api_hash="{}", share_channel_id="{}", session_name="{}", state="{}", start_script="{}"'.format(
    #         self.telegram_id,
    #         self.phone,
    #         self.share_channel_id,
    #         self.session_name,
    #         self.state,
    #         self.start_script,
    #         self.api_id,
    #         self.api_hash,
    #         )
    # def set_telegram_id(telegram_id):
    #     pass
    #
    # def set_api_id_api_hash(self, api_id, api_hash):
    #     self.api_hash = api_hash


#     self.api_id = api_id


# phone=None, api_id=None, api_hash=None, session_name=None, state=None, start_script=None


def get_user(telegram_user_id: int, session_name):
    query = session_db.query(User).filter_by(telegram_id=str(telegram_user_id), session_name=session_name)
    user = query.first()
    if user is None:
        user = User(telegram_id=telegram_user_id, session_name=session_name)
        session_db.add(user)
        session_db.commit()
    return user


def get_user_key(telegram_user_id: int, session_name):
    query = session_db.query(User).filter_by(telegram_id=str(telegram_user_id), session_name=session_name)
    user = query.first()
    if user is None:
        raise NotCorrect('У вас нет такой сессии')
    return user.key_userbot


def get_data(telegram_user_id: int, session_name, arg):
    if arg not in command_get_list:
        raise NotCorrect("arg not in command_get_list")

    user = get_user(telegram_user_id, session_name)
    return getattr(user, arg)


def filter_method(key_userbot, table, column, arg, error_msg=''):
    query = session_db.query(table).filter_by(key_userbot=key_userbot, **{column: arg})
    if query.first() is not None:
        raise DataDuplicateExc(error_msg)


def set_data(telegram_user_id: int, session_name, arg, data):
    if hasattr(User, arg):
        check_arg_dict[arg](data)
        user = get_user(telegram_user_id, session_name)
        setattr(user, arg, data)
    elif hasattr(ParsChannel, arg):
        user_key = get_user_key(telegram_user_id, session_name)
        filter_method(user_key, ShareChannel, 'share_channel_id', data,
                      f"Нельзя добавить ParsChannel: {data}, т.к. он добавлен в ShareChannel")
        filter_method(user_key, ParsChannel, 'pars_channel_id', data,
                      f"ParsChannel: {data} уже добавлен в эту сессию")
        pars_channel = ParsChannel(key_userbot=user_key, pars_channel_id=int(data))
        session_db.add(pars_channel)
    elif hasattr(ShareChannel, arg):
        user_key = get_user_key(telegram_user_id, session_name)
        # check_arg_dict[arg](data)                     # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        filter_method(user_key, ShareChannel, 'share_channel_id', data, f"ShareChannel: {data} уже добавлен в эту сессию")
        filter_method(user_key, ParsChannel, 'pars_channel_id', data, f"Нельзя добавить ShareChannel: {data}, т.к. он добавлен в PostChannel")
        share_channel = ShareChannel(key_userbot=user_key, share_channel_id=int(data))
        session_db.add(share_channel)
    elif hasattr(Ticker, arg):
        user_key = get_user_key(telegram_user_id, session_name)
        filter_method(user_key, Ticker, 'ticker', data,
                      f"Ticker: {data} уже добавлен  в эту сессию")
        ticker = Ticker(key_userbot=user_key, ticker=data)
        session_db.add(ticker)
    elif hasattr(Tag, arg):
        pass
    else:
        raise NotCorrect
    # for arg in (kwargs.keys() & __arg_user_db):
    #     setattr(user, arg, kwargs[arg])  # что будет если во время запуска поменять данные

    session_db.commit()
