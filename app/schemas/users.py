# import basmodel & validator
from pydantic import BaseModel, validator

# import helper validator
from ..utils import validate_not_empty

# helper function to check if password is long enough
def validate_password_length(value):
    if len(value) < 8:
        raise ValueError('must be atleast 8 characters long')

# helper function to check if passwords match
def match_passwords(value, values, password):
    if password in values and values[password] != value:
        raise ValueError(f'not matching with {password}')

# login request basemodel
class Login(BaseModel):
    email: str
    password: str

    # email validator
    @validator('email')
    def validate_email(cls, value):
        validate_not_empty(value)
        return value

    # password validator
    @validator('password')
    def validate_password(cls, value):
        validate_not_empty(value)
        return value


class Register(BaseModel):
    email: str
    password: str
    confirm_password: str

    # email validator
    @validator('email')
    def validate_email(cls, value):
        validate_not_empty(value)
        return value

    # password validator
    @validator('password')
    def validate_password(cls, value):
        validate_not_empty(value)
        validate_password_length(value)
        return value

    # confirm password validator
    @validator('confirm_password')
    def validate_confirm_password(cls, value, values):
        match_passwords(value, values, 'password')
        return value

class UpdatePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
    
    # password validator
    @validator('new_password')
    def validate_new_password(cls, value, values):
        validate_not_empty(value)
        validate_password_length(value)
        if 'old_password' in values and values['old_password'] == value:
            raise ValueError('cannot be same as old_password')
        return value

    # confirm password validator
    @validator('confirm_password')
    def validate_confirm_new_password(cls, value, values):
        match_passwords(value, values, 'new_password')
        return value