from sqlalchemy import Column, Integer, String, TIMESTAMP, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
import datetime
from db.sessions import bot_session as session

Base = declarative_base()


class RegistrationTokens(Base):
    __tablename__ = 'registration_tokens'
    id = Column(Integer, primary_key=True, nullable=False)
    token = Column(String(40), nullable=False)
    used = Column(BOOLEAN, default=False)
    used_by = Column(Integer)
    used_at = Column(TIMESTAMP)
    created_by = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now())
    fresh_until = Column(TIMESTAMP)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_unused_tokens(cls):
        return session.query(cls).filter(cls.used == False, cls.fresh_until > datetime.datetime.now()).all()

    @classmethod
    def add_token(cls, created_by):
        from uuid import uuid4
        token = uuid4().hex
        fresh_until = datetime.datetime.now() + datetime.timedelta(days=1)
        new_token = cls(token=token, created_by=created_by, fresh_until=fresh_until)
        session.add(new_token)
        session.commit()
        return new_token

    @classmethod
    def get_token(cls, token):
        return session.query(cls).filter(cls.token == token, cls.used == False,
                                         cls.fresh_until > datetime.datetime.now()).first()

    def use_token(self, used_by):
        if self.used:
            raise Exception('Token is already used.')
        used_at = datetime.datetime.now()
        self.used_by = used_by
        self.used_at = used_at
        self.used = True
        session.commit()
        return self
