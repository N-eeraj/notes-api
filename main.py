# import and run asgi server
import uvicorn

# load .env
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

host = os.getenv('HOST')

if __name__ == '__main__':
    uvicorn.run('app.api:app', host=host, reload=True)