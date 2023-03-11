# imports for sqlalchemy setup
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from ..db import engine, Base

class User(Base):
    __tablename__ = 'users'

    # table columns
    id = Column('id', Integer, primary_key=True)
    email = Column('email', String(50), unique=True, nullable=False)
    password = Column('password', String(128), nullable=False)

    def __init__ (self, email, password):
        self.id = None
        self.email = email
        self.password = password

    def __repr__ (self):
        return f'({self.id}, {self.email}, {self.password})'


Base.metadata.create_all(bind=engine)