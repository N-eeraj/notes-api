# import httpexception, db, models
from fastapi import HTTPException
from ..db import session
from ..models.users import User
import bcrypt

def login_handler(request):
    validate_login(request.email, request.password)

    # return success message
    return {
        'success': True,
        'message': 'Logged in successfully'
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

def register_handler(request):
    hashed_password = bcrypt.hashpw(bytes(request.password, 'utf-8'), bcrypt.gensalt())
    user = User(request.email, hashed_password)
    session.add(user)
    session.commit()
    return {
        'success': True,
        'message': 'Registration completed successfully'
    }