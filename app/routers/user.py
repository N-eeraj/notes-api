# import apirouter and request
from fastapi import APIRouter, Depends

# import schemas & controller
from ..schemas import users as user_schemas
from ..controllers import users as user_controller

# import auth token validator
from ..auth import verify_auth_token

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
async def logout(user_details: dict = Depends(verify_auth_token)):
    # get token from request headers
    token = user_details['token']

    # remove token from tokens table
    user_controller.remove_token_by_token(token)

    # return response
    return {
        'success': True,
        'message': 'Logout successfull'
    }

# change password api
@router.patch('/change-password')
async def change_password(request: user_schemas.UpdatePassword, user_details: dict = Depends(verify_auth_token)):
    # get user id from request headers
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