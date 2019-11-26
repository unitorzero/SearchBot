from sqlalchemy import Column, Integer, TIMESTAMP, JSON
from sqlalchemy.ext.declarative import declarative_base
import datetime
from db.sessions import bot_session as session
from db.utils import PaginateQuery
from config import PAGINATE_MAX_LEN, PAGINATE_PAGE_LEN

Base = declarative_base()


class Requests(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    date = Column(TIMESTAMP, default=datetime.datetime.now())
    filters = Column(JSON, nullable=False)

    @classmethod
    def add(cls, user_id, filters):
        new_request = cls(user_id=user_id, filters=filters)
        session.add(new_request)
        session.commit()
        return new_request

    @classmethod
    def paginate_left(cls, user_id, first, last):
        return PaginateQuery(session.query(cls).filter(cls.user_id == int(user_id)), cls.id, PAGINATE_PAGE_LEN, first,
                             last, True).prev()

    @classmethod
    def paginate_right(cls, user_id, first, last):
        return PaginateQuery(session.query(cls).filter(cls.user_id == int(user_id)), cls.id, PAGINATE_PAGE_LEN, first,
                             last, True).next()

    @classmethod
    def first_paginate(cls, user_id, first=0, last=0):
        return PaginateQuery(session.query(cls).filter(cls.user_id == int(user_id)), cls.id, PAGINATE_MAX_LEN + 1,
                             first, last, True).next(True)
