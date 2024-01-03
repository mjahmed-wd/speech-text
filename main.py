import os

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from bson.objectid import ObjectId

from model import transcribe_file
import db_connection
from bson import ObjectId

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
async def save_transcribe(payload: TranscribeRequest):
    fileUrl: str = payload.fileUrl
    if not fileUrl:
        raise HTTPException(status_code=400, detail="fileUrl is required")
    result: str = transcribe_file(fileUrl)

    result_dict = {"transcription": result, "fileUrl": fileUrl}

    inserted_id = transcript_collection.insert_one(result_dict).inserted_id
    return {"transcription_id": str(inserted_id)}


@app.post("/search_transcript")
async def search_transcript(transcript_id: str):
    if not transcript_id:
        raise HTTPException(status_code=400, detail="transcript_id is required")
    result = transcript_collection.find_one(ObjectId(transcript_id))
    if not result:
        raise HTTPException(status_code=404, detail="Transcript not found")

    result["_id"] = str(result["_id"])

    return result
