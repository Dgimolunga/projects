# -*- coding: utf-8 -*-
import BOT.test1.Bot_test4.logger as my_logger

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.session import sessionmaker

import re

"""
tools for ParseBot`s ORM database
"""
# from sqlalchemy.ext.declarative import declarative_base

# ____________________________________________________________
# add my logger
logger = my_logger.get_logger(__name__)

# ____________________________________________________________
# for ORM
engine = create_engine('sqlite:///USERBOT_DB.db', echo=True)
Base = declarative_base(engine)
session_db = sessionmaker(bind=engine)()


# ____________________________________________________________
# Exception classes
class NotCorrectExc(Exception):
    pass


class DataDuplicateExc(Exception):
    pass


class UserNotFoundExc(Exception):
    pass


# ____________________________________________________________
# tuple for ParseBotORM columns for classes
arg_user_db = (
    'telegram_id',
    'phone',
    'api_id',
    'api_hash',
    'share_channel_id',
    'start_script'
)
__arg_user_db = (
    'user_logging',
    'phone',
    'api_id',
    'api_hash',
    'share_channel_id',
    'session_name',
    'state',
    'start_script'
)
arg_for_session = (
    'phone',
    'api_id',
    'api_hash',
    'share_channel_id'
)
arg_other = (
    "some arg...."
)
command_set_list = (
    'phone',
    'api_id',
    'api_hash',
    'share_channel_id',
)
command_get_list = (
    'phone',
    'api_id',
    'api_hash',
    'share_channel_id',
)


# ____________________________________________________________
# utils functions
def raise_exc(error):
    raise NotCorrectExc(error)


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


# ____________________________________________________________
# ORM classes
class User(Base):
    __tablename__ = 'Users'
    user_logging = Column(String, primary_key=True)
    user_password = Column(String)
    # telegram_id = Column(Integer)  # а если кто то захочет зарегать
    phone = Column(String)
    api_id = Column(Integer)
    api_hash = Column(String)
    session_name = Column(String)
    # state = Column(String)
    start_script = Column(String)


class TelegramIdHaveUsers(Base):
    __tablename__ = 'Tel_Users'
    key_tel_user = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    key_user = Column(String)


class Ticker(Base):
    __tablename__ = 'Tickers'
    key_ticker = Column(Integer, primary_key=True)
    key_user = Column(String)
    ticker = Column(String)


class Tag(Base):
    __tablename__ = 'Tags'
    key_tag = Column(Integer, primary_key=True)
    key_user = Column(String)
    key_ticker = Column(Integer)
    tag = Column(String)


class ShareChannel(Base):
    __tablename__ = 'ShareChannels'
    key_sharechannel = Column(Integer, primary_key=True)
    key_user = Column(String)
    share_channel_id = Column(Integer)


class ParsChannel(Base):
    __tablename__ = 'ParsChannels'
    key_parschannel = Column(Integer, primary_key=True)
    key_user = Column(String)
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


# ____________________________________________________________
# functions for management ORM database for ParseBot
def check_user_in_telegram_id(user_logging, telegram_id):
    query = session_db.query(TelegramIdHaveUsers).filter_by(key_user=user_logging, telegram_id=telegram_id)
    return query.first()


def add_user_to_telegram_id(user_logging, telegram_id):
    tel_user = TelegramIdHaveUsers(telegram_id=telegram_id, key_user=user_logging)
    session_db.add(tel_user)
    session_db.commit()


def get_user(user_logging, telegram_user_id: int, ):
    if not check_user_in_telegram_id(user_logging, telegram_user_id):
        raise UserNotFoundExc()
    query = session_db.query(User).filter_by(user_logging=user_logging)
    user = query.first()
    return user


#  util for /create_user command
def check_user_logging_name(name: str):
    query = session_db.query(User).filter_by(user_logging=name)
    user = query.first()
    if user is None:
        return True
    else:
        return False


# for /create_user command
def new_user(user_logging: str, hash_, sender_id):
    user = User(user_logging=user_logging, user_password=hash_)
    session_db.add(user)
    session_db.commit()
    add_user_to_telegram_id(user_logging, sender_id)


# for /get commands
def get_data(telegram_user_id: int, user_logging, arg):
    if arg not in command_get_list:
        raise NotCorrectExc("arg not in command_get_list")

    user = get_user(user_logging, telegram_user_id)
    return getattr(user, arg)


# for /my_users command
def get_all_users(telegram_id):
    users_list = []
    query = session_db.query(TelegramIdHaveUsers).filter_by(telegram_id=str(telegram_id))
    for user in query:
        users_list.append(user.key_user)
    return users_list


#  repeatability check for set_data
def filter_method(user_logging, table, column, arg, error_msg=''):
    query = session_db.query(table).filter_by(key_user=user_logging, **{column: arg})
    if query.first() is not None:
        raise DataDuplicateExc(error_msg)


# for /set or /add commands
def set_data(telegram_user_id: int, user_logging, arg, data):
    user = get_user(user_logging, telegram_user_id)

    if hasattr(User, arg):
        check_arg_dict[arg](data)
        setattr(user, arg, data)
    elif hasattr(ParsChannel, arg):
        filter_method(user_logging, ShareChannel, 'share_channel_id', data,
                      f"Нельзя добавить ParsChannel: {data}, т.к. он добавлен в ShareChannel")
        filter_method(user_logging, ParsChannel, 'pars_channel_id', data,
                      f"ParsChannel: {data} уже добавлен в эту сессию")
        pars_channel = ParsChannel(key_user=user_logging, pars_channel_id=int(data))
        session_db.add(pars_channel)
    elif hasattr(ShareChannel, arg):
        # check_arg_dict[arg](data)                     # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        filter_method(user_logging, ShareChannel, 'share_channel_id', data,
                      f"ShareChannel: {data} уже добавлен в эту сессию")
        filter_method(user_logging, ParsChannel, 'pars_channel_id', data,
                      f"Нельзя добавить ShareChannel: {data}, т.к. он добавлен в PostChannel")
        share_channel = ShareChannel(key_user=user_logging, share_channel_id=int(data))
        session_db.add(share_channel)
    elif hasattr(Ticker, arg):
        filter_method(user_logging, Ticker, 'ticker', data,
                      f"Ticker: {data} уже добавлен  в эту сессию")
        ticker = Ticker(key_user=user_logging, ticker=data)
        session_db.add(ticker)
    elif hasattr(Tag, arg):
        pass
    else:
        raise NotCorrectExc
    # for arg in (kwargs.keys() & __arg_user_db):
    #     setattr(user, arg, kwargs[arg])  # что будет если во время запуска поменять данные

    session_db.commit()
