from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from ..db import engine, Base

class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    email = Column('email', String(50), unique=True)
    password = Column('password', String(128))

    def __init__ (self, email, password):
        self.id = None
        self.email = email
        self.password = password

    def __repr__ (self):
        return f'({self.id}, {self.email}, {self.password})'


Base.metadata.create_all(bind=engine)