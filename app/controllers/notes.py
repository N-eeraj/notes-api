# imports
from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound
from ..db import session

# model
from ..models.notes import Note

def save_note_to_db(user_id, title):
    # save note to notes table
    note = Note(user_id, title)
    session.add(note)
    session.commit()
    return note.id

def create_note(id, body):
    # create file and write it's content
    with open(f'notes/{id}.txt', 'w') as file:
        file.write(body)