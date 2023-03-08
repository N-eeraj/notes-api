# imports
from fastapi import HTTPException
from ..db import session
import bcrypt
import secrets

# models
from ..models.users import User
from ..models.tokens import Token

def login_handler(request):
    # validate user using users table
    id = validate_login(request.email, request.password)

    # get bearer token
    token = get_bearer_token(id)

    # return success message
    return {
        'success': True,
        'message': 'Logged in successfully',
        'token': token
    }

def validate_login(email, password):
    # fetch user details by email
    results = session.query(User).filter(User.email == email).all()
    if len(results) == 0:
        raise HTTPException(status_code=401, detail={
            'success':False,
            'message': 'User not found'
        })

    # check request password
    incorrect_password = not bcrypt.checkpw(bytes(password, 'utf-8'), results[0].password.encode('utf-8'))
    if incorrect_password:
        raise HTTPException(status_code=401, detail={
            'success':False,
            'message': 'Incorrect password'
        })
    return results[0].id

def register_handler(request):
    # check if email already exist in users table


    # encrypt password and save to users table
    hashed_password = bcrypt.hashpw(bytes(request.password, 'utf-8'), bcrypt.gensalt())
    user = User(request.email, hashed_password)
    session.add(user)
    session.commit()

    results = session.query(User).filter(User.email == request.email).all()
    id = results[0].id

    # get bearer token
    token = get_bearer_token(id)

    # return response
    return {
        'success': True,
        'message': 'Registration completed successfully',
        'token': token
    }

def get_bearer_token(id):
    # generate bearer token
    jwt_token = secrets.token_hex(32)

    # save token to tokens table
    token = Token(id, jwt_token)
    session.add(token)
    session.commit()

    # return generated token
    return jwt_token