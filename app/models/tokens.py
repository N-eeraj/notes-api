from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from ..db import engine, Base

class Token(Base):
    __tablename__ = 'tokens'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
    token = Column('token', String(32), unique=True, nullable=False)

    def __init__ (self, user_id, token):
        self.id = None
        self.user_id = user_id
        self.token = token

    def __repr__ (self):
        return f'({self.id}, {self.user_id}, {self.token})'


Base.metadata.create_all(bind=engine)