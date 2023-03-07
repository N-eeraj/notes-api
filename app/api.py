# import fastapi & corsmiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# ping api
@app.get('/ping', tags=['Test'])
async def ping():
    return {
        'ping': 'pong'
    }