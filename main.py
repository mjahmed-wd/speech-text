from fastapi import FastAPI, Request
from model import transcribe_file
from fastapi import Request

app = FastAPI()

@app.get("/")
async def index():
    return {"data": "Welcome"}

@app.post("/transcribe")
async def transcribe(request: Request):
    data = await request.json()
    fileUrl = data.get("fileUrl")
    result = transcribe_file(fileUrl)
    return result