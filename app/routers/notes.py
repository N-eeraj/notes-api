# import apirouter and request
from fastapi import APIRouter, Request

# import schemas and controller
from ..schemas import notes as noteSchemas
from ..controllers import notes as noteController

from ..utils import get_user_id

# initialize router
router = APIRouter(prefix='/notes' ,tags=['Notes'])

# create note api
@router.post('/create')
async def create_note(request: noteSchemas.Note):
    print(request)

# edit note api
@router.post('/edit/{id}')
async def edit_note(id: int, request: noteSchemas.Note):
    print(id)
    print(request)