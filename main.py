import os

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from bson.objectid import ObjectId
from llama_index import download_loader, VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
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
    return {"transcription_id": str(inserted_id), "transcription": result, "fileUrl": fileUrl}


@app.post("/summary_from_transcript")
async def summary_from_transcript(transcript_id: str):
    if not transcript_id:
        raise HTTPException(status_code=400, detail="transcript_id is required")
    result = transcript_collection.find_one(ObjectId(transcript_id))
    if not result:
        raise HTTPException(status_code=404, detail="Transcript not found")

    result["_id"] = str(result["_id"])


    JsonDataReader = download_loader("JsonDataReader")
    loader = JsonDataReader()
    documents = loader.load_data(result["transcription"])
    index = VectorStoreIndex.from_documents(documents)

    persist_dir = f'./storage/cache/transcription/{transcript_id}'

    try:
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        index = load_index_from_storage(storage_context)
        print('loading from disk')
    except:
        JsonDataReader = download_loader("JsonDataReader")
        loader = JsonDataReader()
        documents = loader.load_data(result["transcription"])
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=persist_dir)
        print('creating on disk')


    query_engine = index.as_query_engine()
    query_result = query_engine.query("Give me a summary of the speech")

    
    return query_result.response
