# -*- coding: utf-8 -*-
# import sqlite3
#
#
# db_connect = sqlite3.connect("script_db.db")
# cursor = db_connect.cursor()
# cursor.execute("""CREATE TABLE IF NOT EXISTS users
#                     (id INTEGER,
#                     phone text,
#                     api_id integer,
#                     api_hash text,
#                     session_name text,
#                     start text)
#                 """)
# db_connect.commit()
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm.session import sessionmaker

# from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('sqlite:///USERBOT_DB.db', echo=True)
Base = declarative_base(engine)


class UserBot(Base):
    __tablename__ = 'UserBots'
    key_userbot = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)     # а если кто то захочет зарегать
    phone = Column(String)
    api_id = Column(Integer)
    api_hash = Column(String)
    session_name = Column(String)
    state = Column(String)
    start_script = Column(String)
    # parsing_channels =


    # def __repr__(self):
    #     return '<User(telegram_id="{}", phone="{}", api_id="{}", api_hash="{}", share_channel_id="{}", session_name="{}", state="{}", start_script="{}"'.format(
    #         self.telegram_id,
    #         self.phone,
    #         self.api_id,
    #         self.api_hash,
    #         self.share_channel_id,
    #         self.session_name,
    #         self.state,
    #         self.start_script,
    #         )


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



# print(User.__repr__(User))
Base.metadata.create_all(engine)
# sesion = sessionmaker(engine)()
# new_users = User(telegram_id=12345, phone=None, api_id=1111111, api_hash="sfsdf", session_name="session_name_12345", state = "False", start_script="False")
# sesion.add(new_users)
# sesion.commit()
