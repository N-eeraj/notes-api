# import apirouter and request
from fastapi import APIRouter, Request

# import schemas and controller
from ..schemas import notes as note_schemas
from ..controllers import notes as note_controller

from ..utils import get_user_details

# initialize router
router = APIRouter(prefix='/note' ,tags=['Notes'])

# list all user notes
@router.get('/list')
async def list_notes(http_request: Request, page: int=1):
    # validate page number
    note_controller.validate_page_number(page)

    # get user id
    user_id = get_user_details(http_request)['user_id']

    # fetch number of notes of the user
    total_notes_count = note_controller.get_notes_count(user_id)

    # check if page number exists
    note_controller.check_page_existance(page, total_notes_count)

    # fetch all notes of the user
    user_notes = note_controller.fetch_all_user_notes(user_id, page)

    # get all details to return
    notes = []
    for note in user_notes:
        body = note_controller.read_note_file(note.id)
        if len(body) > 100:
            body = f'{body[:100]}...'
        notes.append({
            'id': note.id,
            'title': note.title,
            'body': body
        })

    # return response
    return {
        'success': True,
        'message': 'Notes fetched successfully',
        'data': {
            'notes': notes,
            'total_count': total_notes_count
        }
    }

# create note api
@router.post('/create')
async def create_note(request: note_schemas.Note, http_request: Request):
    # get user id
    user_id = get_user_details(http_request)['user_id']

    # save entry to db
    note_id = note_controller.save_note_to_db(user_id, request.title)

    # create note file
    note_controller.create_note(note_id, request.body)

    # return response
    return {
        'success': True,
        'message': 'Created note successfully'
    }

# read note api
@router.get('/{id}')
async def read_note(id: int, http_request: Request):
    # get user id
    user_id = get_user_details(http_request)['user_id']

    # fetch note details from db
    note = note_controller.find_note(id, user_id).one()

    # get note body
    body = note_controller.read_note_file(id)

    # return response
    return {
        'success': True,
        'message': 'Note fetched successfully',
        'data': {
            'id': id,
            'title': note.title,
            'body': body
        }
    }

# update note api
@router.put('/update/{id}')
async def update_note(id: int, request: note_schemas.Note, http_request: Request):
    # get user id
    user_id = get_user_details(http_request)['user_id']

    # find note
    note_id = note_controller.find_note_and_update_title(id, user_id, request.title)

    # update note file
    note_controller.create_note(note_id, request.body)

    # return response
    return {
        'success': True,
        'message': 'Note updated successfully'
    }

# delete note api
@router.delete('/delete/{id}')
async def delete_note(id: int, http_request: Request):
    # get user id
    user_id = get_user_details(http_request)['user_id']

    # delete entry from db
    note_controller.delete_note_from_db(id, user_id)

    # delete note file
    note_controller.delete_note(id)

    # return response
    return {
        'success': True,
        'message': 'Note deleted successfully'
    }