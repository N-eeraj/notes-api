from pydantic import BaseModel, validator

# helper function to check for empty strings
def not_empty(value):
    if value == '':
        raise ValueError('cannot be empty')
    return value

# login request basemodel
class Login(BaseModel):
    email: str
    password: str

    # email validator
    @validator('email')
    def email_not_empty(cls, value):
        return not_empty(value)

    # password validator
    @validator('password')
    def password_not_empty(cls, value):
        return not_empty(value)