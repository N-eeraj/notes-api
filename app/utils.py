from .controllers import users as userControllers

# function to get user id & token from request header
def get_user_id(request):
    token = request.headers['authorization'][7:]
    user_id = userControllers.validate_token(token)
    return {
        'token': token,
        'user_id': user_id
    }

# helper function to check for empty strings
def validate_not_empty(value):
    if value == '':
        raise ValueError('cannot be empty')