# import apirouter
from fastapi import APIRouter

# import model
from ..schemas import users as userSchemas
from ..controllers import users as userControllers

# initialize router
router = APIRouter()

# login api
@router.post('/login', tags=['Users'])
async def test(request: userSchemas.Login):
    return userControllers.login_handler(request)

# register api
@router.post('/register', tags=['Users'])
async def test(request: userSchemas.Register):
    return userControllers.register_handler(request)