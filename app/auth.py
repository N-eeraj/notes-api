from fastapi import Request, HTTPException

# import user details helper
from .utils import get_user_details

async def verify_auth_token(http_request: Request):
    user_details = get_user_details(http_request)
    if user_details and user_details['token'] :
        if user_details['user_id']:
            return user_details
        else:
            raise HTTPException(status_code=401, detail={
                'success': False,
                'message': 'Invalid auth token'
            })
    else:
        raise HTTPException(status_code=401, detail={
            'success': False,
            'message': 'Missing auth token'
        })