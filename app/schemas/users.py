from pydantic import BaseModel, validator

# helper function to check for empty strings
def validate_not_empty(value):
    if value == '':
        raise ValueError('cannot be empty')

# helper function to check if password is long enough
def validate_password_length(value):
    if len(value) < 8:
        raise ValueError('must be atleast 8 characters long')

# helper function to check if password is long enough
def match_passwords(value, values, password):
    if password in values and values[password] != value:
        raise ValueError(f'not matching with {password}')

# login request basemodel
class Login(BaseModel):
    email: str
    password: str

    # email validator
    @validator('email')
    def email_not_empty(cls, value):
        validate_not_empty(value)
        return value

    # password validator
    @validator('password')
    def password_not_empty(cls, value):
        validate_not_empty(value)
        return value


class Register(BaseModel):
    email: str
    password: str
    confirm_password: str

    # email validator
    @validator('email')
    def email_not_empty(cls, value):
        validate_not_empty(value)
        return value

    # password validator
    @validator('password')
    def password_not_empty(cls, value):
        validate_not_empty(value)
        validate_password_length(value)
        return value

    # confirm password validator
    @validator('confirm_password')
    def confirm_password_not_empty(cls, value, values):
        match_passwords(value, values, 'password')
        return value

class UpdatePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
    
    # password validator
    @validator('new_password')
    def password_not_empty(cls, value, values):
        validate_not_empty(value)
        validate_password_length(value)
        if 'old_password' in values and values['old_password'] == value:
            raise ValueError('cannot be same as old_password')
        return value

    # confirm password validator
    @validator('confirm_password')
    def confirm_password_not_empty(cls, value, values):
        match_passwords(value, values, 'new_password')
        return value