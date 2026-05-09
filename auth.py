from fastapi import FastAPI

app = FastAPI()

@app.get('/auth/')
async def auth():
    return {"user": "authenticated"}