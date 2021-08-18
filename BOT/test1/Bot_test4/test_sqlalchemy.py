# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm.session import sessionmaker

# from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///USERBOT_test_DB.db', echo=True)
Base = declarative_base(engine)

set_user_db = [
    'telegram_id',
    'phone',
    'api_id',
    'api_hash',
    'session_name',
    'state,',
    'start_script'
]


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    phone = Column(String)
    api_id = Column(Integer)
    api_hash = Column(String)
    session_name = Column(String)
    state = Column(String)
    start_script = Column(String)

    # def __repr__(self):
    #     return '<User(telegram_id="{}", phone="{}", api_id="{}", api_hash="{}", session_name="{}", state="{}", start_script="{}"'.format(
    #         self.telegram_id,
    #         self.phone,
    #         self.api_id,
    #         self.api_hash,
    #         self.session_name,
    #         self.state,
    #         self.start_script,
    #     )

    # def set_telegram_id(telegram_id):
    #     pass
    #
    # def set_api_id_api_hash(self, api_id, api_hash):
    #     self.api_hash = api_hash
    #     self.api_id = api_id


Base.metadata.create_all(engine)
session_db = sessionmaker(bind=engine)()


# phone=None, api_id=None, api_hash=None, session_name=None, state=None, start_script=None


def set_data(telegram_user_id: int, **kwargs):
    query = session_db.query(User).filter_by(telegram_id=telegram_user_id)
    user = query.first()
    if user is None:
        user = User(telegram_id=telegram_user_id)
        session_db.add(user)
        session_db.commit()

    for i in (kwargs.keys() & set_user_db):
        setattr(user, i, kwargs[i])  # что будет если во время запуска поменять данные

    session_db.commit()


set_data(123123, phone='79525262055')
d = {'phone': '11111111', 'api_id': '222222222'}
set_data(3223, api_hash='wwwwwwwwwww', **d)


def test():
    q = session_db.query(User).filter_by(telegram_id='12345123342')
    print("aaaaaa!~~~~~~~~~~~~~~~~~~~~~~~~~~")
    data = "1234"
    user = q.first()
    if user is None:
        new_user = User(telegram_id=12345123)
        session_db.add(new_user)
        session_db.commit()
    else:
        user.api_hash = data
        session_db.commit()

# new_users = User(telegram_id=12345, phone="1233231", api_id=1111111, api_hash="sfsdf", session_name="session_name_12345", state = "False", start_script="False")
# session_db.add(new_users)
# session_db.commit()
# print(q.first() is None)
# base = declarative_base()
#
# class Topic(base):
#
#     __tablename__ = 'topic'
#
#     __tableargs__ = {
#         'comment': 'Темы цитат'
#
#     }
#
#     topic_id = sqlalchemy.Column(
#         sqlalchemy.Integer,
#         nullable=False,
#         unique=True,
#         primary_key=True,
#         autoincrement=True
#     )
