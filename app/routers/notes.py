# import apirouter and request
from fastapi import APIRouter, Request

# import schemas and controller
from ..schemas import notes as noteSchemas
from ..controllers import notes as noteController

from ..utils import get_user_details

# initialize router
router = APIRouter(prefix='/notes' ,tags=['Notes'])

# create note api
@router.post('/create')
async def create_note(request: noteSchemas.Note, http_request: Request):
    # get user id
    user_id = get_user_details(http_request)['user_id']

    # save entry to db
    note_id = noteController.save_note_to_db(user_id, request.title)

    # create note file
    noteController.create_note(note_id, request.body)

    # return response
    return {
        'success': True,
        'message': 'Created note successfully'
    }

# edit note api
@router.post('/edit/{id}')
async def edit_note(id: int, request: noteSchemas.Note):
    print(id)
    print(request)