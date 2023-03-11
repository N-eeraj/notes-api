from .controllers import users as user_controllers

# function to get user id & token from request header
def get_user_details(request):
    token = request.headers['authorization'][7:]
    user_id = user_controllers.validate_token(token)
    return {
        'token': token,
        'user_id': user_id
    }

# helper function to check for empty strings
def validate_not_empty(value):
    if value == '':
        raise ValueError('cannot be empty')