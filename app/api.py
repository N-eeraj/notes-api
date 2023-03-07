from fastapi import FastAPI

app = FastAPI()

@app.get('/ping', tags=['test'])
def ping():
    return {
        'ping': 'pong'
    }