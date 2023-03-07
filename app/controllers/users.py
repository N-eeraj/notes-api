# import httpexception
from fastapi import HTTPException

def login_handler(request):
    validate_login(request.email, request.password)

    # return success message
    return {
        'success': True,
        'message': 'Logged in successfully'
    }

def validate_login(email, password):
    # check request (temporarily with static value)
    if email != 'test@example.com':
        raise HTTPException(status_code=401, detail={
            'success':False,
            'message': 'User not found'
        })

    # check request password (temporarily with static value)
    if password != '12345678':
        raise HTTPException(status_code=401, detail={
            'success':False,
            'message': 'Incorrect password'
        })

def register_handler(request):
    return {
        'success': True,
        'message': 'Registration completed successfully'
    }