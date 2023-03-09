# imports
from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound
from ..db import session
import bcrypt
import secrets

# models
from ..models.users import User
from ..models.tokens import Token

def get_hashed_password(password):
    # return hash of password argument
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

def validate_login(email, password):
    try:
        # fetch user details by email
        result = session.query(User).filter(User.email==email).one()
    except NoResultFound:
        # respond with error if email is not found
        raise HTTPException(status_code=404, detail={
            'success':False,
            'message': 'User not found'
        })

    # check request password
    incorrect_password = not bcrypt.checkpw(bytes(password, 'utf-8'), result.password.encode('utf-8'))
    if incorrect_password:
        # respond with error if password is incorrect
        raise HTTPException(status_code=401, detail={
            'success':False,
            'message': 'Incorrect password'
        })
    return result.id

def create_user(email, password):
    # generate hashed password
    hashed_password = get_hashed_password(password)

    # save new user to users table
    user = User(email, hashed_password)
    session.add(user)
    session.commit()


def check_token_exist(token):
    # check if generated token exists in tokens table
    try:
        results = session.query(Token).filter(Token.token==token).all()
        if len(results):
            return True
    except NoResultFound:
        False

def get_bearer_token(id):
    # generate bearer token
    jwt_token = secrets.token_hex(32)

    # if new token exists in tokens table generate new token and repeat
    if check_token_exist(jwt_token):
        return get_bearer_token(id)

    # save token to tokens table
    token = Token(id, jwt_token)
    session.add(token)
    session.commit()

    # return generated token
    return jwt_token

def check_email_exist(email):
    # check if email exists in users table
    try:
        results = session.query(User).filter(User.email==email).all()
        if len(results):
            raise HTTPException(status_code=409, detail= {
                'success': False,
                'message': 'Email already registered'
            })
    except NoResultFound:
        pass

def validate_token(token):
    # validate if token is in tokens table
    try:
        result = session.query(Token).filter(Token.token==token).one()
        return result.user_id
    except NoResultFound:
        return False


def remove_token_by_token(token):
    # delete token from tokens table
    session.query(Token).filter(Token.token==token).delete()
    session.commit()