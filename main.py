import os

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from model import transcribe_file
import db_connection

db, transcript_collection = db_connection.connect_to_mongodb()

app = FastAPI()

class TranscribeRequest(BaseModel):
    fileUrl: str


@app.get("/")
async def index():
    return {"data": "Welcome"}


@app.post("/transcribe")
async def transcribe(payload: TranscribeRequest):
    fileUrl: str = payload.fileUrl
    if not fileUrl:
        raise HTTPException(status_code=400, detail="fileUrl is required")
    result: str = transcribe_file(fileUrl)

    return result


@app.post("/save_transcribe")
async def transcribe(payload: TranscribeRequest):
    fileUrl: str = payload.fileUrl
    if not fileUrl:
        raise HTTPException(status_code=400, detail="fileUrl is required")
    result: str = transcribe_file(fileUrl)

    result_dict = {"transcription": result}

    inserted_id = transcript_collection.insert_one(result_dict).inserted_id
    return {"transcription_id": str(inserted_id)}
