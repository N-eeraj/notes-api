# import basmodel & validator
from pydantic import BaseModel, validator

# import helper validator
from ..utils import validate_not_empty

class Note(BaseModel):
    title: str
    body: str

    # title validator
    @validator('title')
    def validate_title(cls, value):
        validate_not_empty(value)
        return value

    # body validator
    @validator('body')
    def validate_body(cls, value):
        validate_not_empty(value)
        return value