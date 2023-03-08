# imports
from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound
from ..db import session
import bcrypt
import secrets

# models
from ..models.users import User
from ..models.tokens import Token

def validate_login(email, password):
    # fetch user details by email
    try:
        result = session.query(User).filter(User.email==email).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail={
            'success':False,
            'message': 'User not found'
        })

    # check request password
    incorrect_password = not bcrypt.checkpw(bytes(password, 'utf-8'), result.password.encode('utf-8'))
    if incorrect_password:
        raise HTTPException(status_code=401, detail={
            'success':False,
            'message': 'Incorrect password'
        })
    return result.id

def create_user(email, password):
    hashed_password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    user = User(email, hashed_password)
    session.add(user)
    session.commit()

def get_bearer_token(id):
    # generate bearer token
    jwt_token = secrets.token_hex(32)

    if check_token_exist(jwt_token):
        return get_bearer_token(id)

    # save token to tokens table
    token = Token(id, jwt_token)
    session.add(token)
    session.commit()

    # return generated token
    return jwt_token

def check_email_exist(email):
    try:
        results = session.query(User).filter(User.email==email).all()
        if len(results):
            raise HTTPException(status_code=409, detail= {
                'success': False,
                'message': 'Email already registered'
            })
    except NoResultFound:
        pass

def check_token_exist(token):
    try:
        results = session.query(Token).filter(Token.token==token).all()
        if len(results):
            return True
    except NoResultFound:
        False