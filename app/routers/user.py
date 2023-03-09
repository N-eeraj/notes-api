# import apirouter
from fastapi import APIRouter, Request

# import schemas & controllers
from ..schemas import users as userSchemas
from ..controllers import users as userControllers

from ..utils import get_user_id

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

# logout api
@router.post('/logout', tags=['Users'])
async def logout(http_request: Request):
    # get token from request headers
    token = get_user_id(http_request)['token']

    # remove token from tokens table
    userControllers.remove_token_by_token(token)

    # return response
    return {
        'success': True,
        'message': 'Logout successfull'
    }

# update password api
@router.put('/update-password', tags=['Users'])
async def update_password(http_request: Request, request: userSchemas.UpdatePassword):
    # get user id from request headers
    user_id = get_user_id(http_request)['user_id']

    # validate old password
    userControllers.validate_old_password(user_id, request.old_password)

    # return response
    return {
        'success': True,
        'message': 'Password updated successfully'
    }