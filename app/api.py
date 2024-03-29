# fastapi imports
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# access user controller for token validation
from .controllers import users as user_controllers

# import api routers
from .routers import user, notes

# load .env
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

origins = os.getenv('ALLOWED_ORIGINS').split(',')

# setup fastapi app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(user.router)
app.include_router(notes.router)

# exception handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        errors = []
        for error in exc.errors():
            errors.append(f"{error['loc'][1]} {error['msg']}")
    except:
        errors = exc
    return JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
        content = jsonable_encoder({
            'message': errors,
            'success': False
        })
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(exc.detail, status_code=exc.status_code)

# ping api
@app.get('/ping', tags=['Test'])
async def ping():
    return {
        'ping': 'pong'
    }