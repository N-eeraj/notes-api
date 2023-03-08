from .controllers import users as userControllers

def get_user_id(request):
    token = request.headers['authorization'][7:]
    user_id = userControllers.validate_token(token)
    return {
        'token': token,
        'user_id': user_id
    }