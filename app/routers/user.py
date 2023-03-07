# import apirouter
from fastapi import APIRouter

# import model
from ..models import users as userModels
from ..controllers import users as userControllers

# initialize router
router = APIRouter()

# login api
@router.post('/login', tags=['Users'])
async def test(request: userModels.Login):
    # handle login
    return userControllers.login_handler(request)