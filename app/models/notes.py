# imports for sqlalchemy setup
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from ..db import engine, Base

class Note(Base):
    __tablename__ = 'notes'

    # table columns
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
    title = Column('title', String(50), index=True, nullable=False)

    def __init__(self, user_id, title):
        self.id = None
        self.user_id = user_id
        self.title = title

    def __repr__(self):
        return f'({self.id}, {self.user_id}, {self.title})'

Base.metadata.create_all(bind=engine)