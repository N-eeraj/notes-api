# import apirouter
from fastapi import APIRouter

# import model
from ..schemas import users as userSchemas
from ..controllers import users as userControllers

# initialize router
router = APIRouter()

# login api
@router.post('/login', tags=['Users'])
async def login(request: userSchemas.Login):
    # validate user using users table
    id = userControllers.validate_login(request.email, request.password)

    # get bearer token
    token = userControllers.get_bearer_token(id)

    # return success message
    return {
        'success': True,
        'message': 'Logged in successfully',
        'token': token
    }

# register api
@router.post('/register', tags=['Users'])
async def register(request: userSchemas.Register):
    # check if email already exist in users table
    userControllers.check_email_exist(request.email)

    # encrypt password and save to users table
    userControllers.create_user(request.email, request.password)

    # get bearer token
    id = userControllers.validate_login(request.email, request.password)
    token = userControllers.get_bearer_token(id)

    # return response
    return {
        'success': True,
        'message': 'Registration completed successfully',
        'token': token
    }