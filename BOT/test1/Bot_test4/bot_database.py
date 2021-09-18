# -*- coding: utf-8 -*-
import BOT.test1.Bot_test4.logger as my_logger
import BOT.test1.Bot_test4.data_value as data_value_file

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.session import sessionmaker

import re

"""
tools for ParseBot`s ORM database
"""
none_ticker = 'No Ticker'
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
    key_user = Column(String, primary_key=True)
    user_password = Column(String)
    # telegram_id = Column(Integer)  # а если кто то захочет зарегать
    # phone = Column(String)
    # api_id = Column(Integer)
    # api_hash = Column(String)
    # session_name = Column(String)
    # state = Column(String)
    # start_script = Column(String)


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


Base.metadata.create_all(engine)

# ____________________________________________________________
# tuple for ParseBotORM columns for classes
arg_other = (
    "some arg...."
)
command_add_list = ('sharechannels', 'parsechannels', 'ticker', 'tag')
command_get_list = ('sharechannels', 'parsechannels', 'tickers', 'tags', 'alltags')

command_set_dict = {'sharechannels': (ShareChannel, 'share_channel_id'),
                    'parsechannels': (ParsChannel, 'pars_channel_id'),
                    'ticker': (Ticker, 'ticker'),
                    'tag': (Tag, 'tag'),
                    }
command_get_dict = {'sharechannels': (ShareChannel, 'share_channel_id'),
                    'parsechannels': (ParsChannel, 'pars_channel_id'),
                    'tickers': (Ticker, 'ticker'),
                    'tags': Tag,
                    'alltags': Tag,
                    }


# ____________________________________________________________
# dict for parse chanel
def add_tag_to_searches_dicts(tag, key_user):
    if tag in data_value_file.tags_of_user:
        data_value_file.tags_of_user[tag].append(key_user)
    else:
        data_value_file.tags_of_user[tag] = [key_user, ]
    if key_user in data_value_file.users_tags:
        data_value_file.users_tags[key_user].append(tag)
    else:
        data_value_file.users_tags[key_user] = [tag, ]


# ____________________________________________________________
# functions for management ORM database for ParseBot
def filter_method_available_in_db(table, **kwargs):
    query = session_db.query(table).filter_by(**kwargs)
    return query


#  repeatability check for set_data
def filter_method_duplicate(table, error_msg='', **kwargs):
    query = filter_method_available_in_db(table, **kwargs)
    if query.first() is not None:
        raise DataDuplicateExc(error_msg)


def check_user_in_telegram_id(user_logging, telegram_id):
    query = session_db.query(TelegramIdHaveUsers).filter_by(key_user=user_logging, telegram_id=telegram_id)
    return query.first()


# _________________________
# add to database methods
def add_parse_channel_to_database(user_logging, data):
    filter_method_duplicate(ShareChannel, f"Нельзя добавить ParsChannel: {data}, т.к. он добавлен в ShareChannel",
                            key_user=user_logging, share_channel_id=data)
    filter_method_duplicate(ParsChannel, f"ParsChannel: {data} уже добавлен в эту сессию",
                            key_user=user_logging, pars_channel_id=data)
    pars_channel_obj = ParsChannel(key_user=user_logging, pars_channel_id=int(data))
    session_db.add(pars_channel_obj)


def add_share_channel_to_database(user_logging, data):
    # check_arg_dict[arg](data)                     # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    filter_method_duplicate(ShareChannel, f"ShareChannel: {data} уже добавлен в эту сессию",
                            key_user=user_logging, share_channel_id=data)
    filter_method_duplicate(ParsChannel, f"Нельзя добавить ShareChannel: {data}, т.к. он добавлен в PostChannel",
                            key_user=user_logging, pars_channel_id=data)
    share_channel_obj = ShareChannel(key_user=user_logging, share_channel_id=int(data))
    session_db.add(share_channel_obj)


def add_tag_to_database(user_logging, ticker_name, data):
    # check Ticker
    query = session_db.query(Ticker).filter_by(key_user=user_logging, ticker=ticker_name)
    if query.first() is None:
        raise NotCorrectExc(f'Ticker: {ticker_name} not found')
    # check tag
    filter_method_duplicate(Tag, f"Tag: {data} уже добавлен в эту папку", key_ticker=query.first().key_ticker, tag=data)
    tag_obj = Tag(key_ticker=query.first().key_ticker, tag=data)
    session_db.add(tag_obj)


def add_ticker_to_database(user_logging, ticker: str = none_ticker):
    filter_method_duplicate(Ticker, 'ticker yet is in database', key_user=user_logging, ticker=ticker, )
    ticker_obj = Ticker(key_user=user_logging, ticker=ticker)
    session_db.add(ticker_obj)
    session_db.commit()


def add_user_to_telegram_id(user_logging, telegram_id):
    tel_user = TelegramIdHaveUsers(telegram_id=telegram_id, key_user=user_logging)
    session_db.add(tel_user)
    session_db.commit()


# for /create_user command
def add_new_user_to_database(user_logging: str, hash_, sender_id):
    user_obj = User(key_user=user_logging, user_password=hash_)
    session_db.add(user_obj)
    add_user_to_telegram_id(user_logging, sender_id)
    add_ticker_to_database(user_logging, none_ticker)
    session_db.commit()


def get_user(user_logging, telegram_user_id: int, ):
    if not check_user_in_telegram_id(user_logging, telegram_user_id):
        raise UserNotFoundExc()
    query = session_db.query(User).filter_by(key_user=user_logging)
    user = query.first()
    return user


#  util for /create_user command
def check_user_logging_name(name: str):
    query = session_db.query(User).filter_by(key_user=name)
    user = query.first()
    if user is None:
        return True
    else:
        return False


# for /get commands
def get_data(telegram_user_id: int, user_logging, arg):
    if not check_user_in_telegram_id(user_logging, telegram_user_id):
        raise UserNotFoundExc()
    return_list = []
    # check for get tag in ticker
    args = arg.split('_', maxsplit=1)
    if len(args) == 1:
        ticker_name = none_ticker
        arg = args[0]
    else:
        ticker_name = args[0]
        arg = args[1]

    if arg not in command_get_dict:
        raise NotCorrectExc(f"{arg} not in command_get_list")

    if arg != 'tags' and arg != 'alltags':
        list_of_obj = session_db.query(command_get_dict[arg][0]).filter_by(key_user=user_logging)
        for obj in list_of_obj:
            return_list.append(getattr(obj, command_get_dict[arg][1]))
        return return_list
    elif arg == 'tags':
        # check ticker in d
        query = filter_method_available_in_db(Ticker, key_user=user_logging, ticker=ticker_name)
        if query.first() is None:
            raise NotCorrectExc(f'Ticker: {ticker_name} not found')
        key_ticker = query.first().key_ticker
        query = session_db.query(Tag).filter_by(key_ticker=key_ticker)
        for tag_obj in query:
            return_list.append(tag_obj.tag)
        return return_list
    elif arg == 'alltags':
        query_ticker = filter_method_available_in_db(Ticker, key_user=user_logging)
        for ticker_obj in query_ticker:
            query_tag = filter_method_available_in_db(Tag, key_ticker=ticker_obj.key_ticker)
            str_to_return_list = f'{ticker_obj.ticker}: '
            list_for_str_to_return_list = []
            for tag_obj in query_tag:
                list_for_str_to_return_list.append(tag_obj.tag)
            str_to_return_list += str(list_for_str_to_return_list)
            return_list.append(str_to_return_list)
        return return_list
    else:
        raise NotCorrectExc


# for /my_users command
def get_all_users(telegram_id):
    users_list = []
    query = session_db.query(TelegramIdHaveUsers).filter_by(telegram_id=str(telegram_id))
    for user in query:
        users_list.append(user.key_user)
    return users_list


# for /set or /add commands
def set_data(telegram_user_id: int, user_logging, arg, data):
    user = get_user(user_logging, telegram_user_id)
    # /add_loggingname_ticker_tag
    # /add_loggingname_tag    ---- Ticker = 'No Ticker'
    args = arg.split('_', maxsplit=1)
    if len(args) == 1:
        ticker_name = none_ticker
        arg = args[0]
    else:
        ticker_name = args[0]
        arg = args[1]

    if hasattr(User, arg):
        check_arg_dict[arg](data)
        setattr(user, arg, data)
    elif hasattr(ParsChannel, arg):
        add_parse_channel_to_database(user_logging, data)
    elif hasattr(ShareChannel, arg):
        add_share_channel_to_database(user_logging, data)
    elif hasattr(Ticker, arg):
        add_ticker_to_database(user_logging, data)
    elif hasattr(Tag, arg):
        add_tag_to_database(user_logging, ticker_name, data)
    else:
        raise NotCorrectExc
    # for arg in (kwargs.keys() & __arg_user_db):
    #     setattr(user, arg, kwargs[arg])  # что будет если во время запуска поменять данные

    session_db.commit()
