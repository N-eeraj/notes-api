# imports
from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound
from ..db import session

# model
from ..models.notes import Note

def find_note(id, user_id):
    # fetch note details from notes table
    try:
        return session.query(Note).filter(Note.id==id, Note.user_id==user_id).one()
    except NoResultFound:
        # respond with error if note is not found under the user
        raise HTTPException(status_code=404, detail={
            'success': False,
            'message': 'File not found'
        })

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

def find_note_and_update_title(id, user_id, title):
    # find an return note id
    note = find_note(id, user_id)
    if note.title != title:
        # update title if needed
        note.title = title
        session.commit()
    return note.id

def read_note_file(id):
    with open(f'notes/{id}.txt', 'r') as file:
        return file.read()