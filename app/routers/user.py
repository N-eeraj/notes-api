# import apirouter and request
from fastapi import APIRouter, Request

# import schemas & controller
from ..schemas import users as user_schemas
from ..controllers import users as user_controller

# import user details helper
from ..utils import get_user_details

# initialize router
router = APIRouter(tags=['Users'])

# login api
@router.post('/login')
async def login(request: user_schemas.Login):
    # validate user using users table
    id = user_controller.validate_login(request.email, request.password)

    # get bearer token
    token = user_controller.get_bearer_token(id)

    # return success message
    return {
        'success': True,
        'message': 'Logged in successfully',
        'token': token
    }

# register api
@router.post('/register')
async def register(request: user_schemas.Register):
    # check if email already exist in users table
    user_controller.check_email_exist(request.email)

    # encrypt password and save to users table
    user_controller.create_user(request.email, request.password)

    # get bearer token
    id = user_controller.validate_login(request.email, request.password)
    token = user_controller.get_bearer_token(id)

    # return response
    return {
        'success': True,
        'message': 'Registration completed successfully',
        'token': token
    }

# logout api
@router.post('/logout')
async def logout(http_request: Request):
    # get token from request headers
    token = get_user_details(http_request)['token']

    # remove token from tokens table
    user_controller.remove_token_by_token(token)

    # return response
    return {
        'success': True,
        'message': 'Logout successfull'
    }

# update password api
@router.put('/update-password')
async def update_password(http_request: Request, request: user_schemas.UpdatePassword):
    # get user id from request headers
    user_details = get_user_details(http_request)
    user_id = user_details['user_id']
    token = user_details['token']

    # validate old password
    user_controller.validate_old_password(user_id, request.old_password)

    # update new password in users table
    user_controller.update_new_password(user_id, request.new_password)

    # remove all tokens of the users except current token
    user_controller.remove_token_by_id(user_id, token)

    # return response
    return {
        'success': True,
        'message': 'Password updated successfully'
    }