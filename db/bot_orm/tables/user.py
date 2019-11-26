from sqlalchemy import Column, Integer, String, TIMESTAMP, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
import datetime
from db.sessions import bot_session as session
from logs import auth_logger
from db.utils import PaginateQuery
from config import PAGINATE_MAX_LEN, PAGINATE_PAGE_LEN

Base = declarative_base()


class User(Base):
    __tablename__ = 'bot_user'
    id = Column(Integer, primary_key=True, nullable=False)
    telegram_id = Column(Integer, nullable=False)
    username = Column(String(200))
    first_name = Column(String(200))
    last_name = Column(String(200))
    registration = Column(TIMESTAMP, default=datetime.datetime.now())
    admin = Column(BOOLEAN)
    deleted = Column(BOOLEAN, default=False)
    description = Column(String(200))

    def as_dict(self):
        dict_result = {}
        for c in self.__table__.columns:
            column = getattr(self, c.name)
            column_name = c.name
            if isinstance(column, datetime.datetime):
                column = str(column)
            dict_result[column_name] = column

        return dict_result

    @classmethod
    def all(cls):
        return session.query(cls).filter(cls.deleted == False).all()

    def __str__(self):
        return 'id:%s, tg_id:%s, username: %s' % (self.id, self.telegram_id, self.username)

    @classmethod
    def get(cls, _id):
        return session.query(cls).filter(cls.id == _id).first()

    @classmethod
    def paginate_left(cls, first, last):
        return PaginateQuery(session.query(cls).filter(cls.deleted == False, cls.admin == None), cls.id,
                             PAGINATE_PAGE_LEN, first, last).prev()

    @classmethod
    def paginate_right(cls, first, last):
        return PaginateQuery(session.query(cls).filter(cls.deleted == False, cls.admin == None), cls.id,
                             PAGINATE_PAGE_LEN, first, last).next()

    @classmethod
    def first_paginate(cls, first=0, last=0):
        return PaginateQuery(session.query(cls).filter(cls.deleted == False, cls.admin == None), cls.id,
                             PAGINATE_MAX_LEN + 1, first, last).next()

    @classmethod
    def users_telegram_keys(cls):
        return {user.telegram_id: user.as_dict() for user in session.query(cls).all()}

    @classmethod
    def admins_telegram_keys(cls):
        return {user.telegram_id: user.as_dict() for user in session.query(cls).filter(cls.admin).all()}

    @classmethod
    def create(cls, telegram_id, username, first_name, last_name):
        new_user = cls(telegram_id=telegram_id, username=username, first_name=first_name, last_name=last_name)
        session.add(new_user)
        session.commit()
        auth_logger.info('New user %s' % (str(new_user)))
        return new_user

    @classmethod
    def delete(cls, _id):
        user = session.query(cls).filter(cls.id == int(_id)).update({cls.deleted: True})
        session.commit()
        return user

    @classmethod
    def add_description(cls, _id, description):
        user = session.query(cls).filter(cls.id == int(_id)).update({cls.description: description})
        session.commit()
        return user
