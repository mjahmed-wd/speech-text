from fastapi import FastAPI
from model import transcribe_file
import uvicorn

app = FastAPI()

@app.get("/")
async def index():
    return {"data": "Welcome"}

@app.get("/transcribe/{fileName}")
async def transcribe(fileName: str):
    result = transcribe_file(fileName)
    return {"data": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8342)
