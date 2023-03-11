# import apirouter and request
from fastapi import APIRouter, Request

# import schemas and controller
from ..schemas import notes as note_schemas
from ..controllers import notes as note_controller

from ..utils import get_user_details

# initialize router
router = APIRouter(prefix='/notes' ,tags=['Notes'])

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