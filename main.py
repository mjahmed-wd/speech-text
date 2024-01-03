from bson import ObjectId
from bson.objectid import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import db_connection
from chat import create_chat_engine, create_index_and_query
from model import transcribe_file

db, transcript_collection, chat_collection = db_connection.connect_to_mongodb()

app = FastAPI()

class TranscribeRequest(BaseModel):
    fileUrl: str
    create_chat_id: bool = False

class AgentQuestionRequest(BaseModel):
    transcript_id: str
    question: str

class Agent2QuestionRequest(BaseModel):
    chat_id: str
    question: str

chat_engines = {}  

@app.post("/summary_from_transcript")
async def save_transcribe(payload: TranscribeRequest):
    fileUrl: str = payload.fileUrl
    if not fileUrl:
        raise HTTPException(status_code=400, detail="fileUrl is required")
    transcription: str = transcribe_file(fileUrl)

    result_dict = {"transcription": transcription, "fileUrl": fileUrl}

    inserted_id = transcript_collection.insert_one(result_dict).inserted_id
    index = create_index_and_query(str(inserted_id), transcription)
    query_engine = index.as_query_engine()
    query_result = query_engine.query(f"Summarize the following. \nTranscript: {transcription}")

    if payload.create_chat_id:
        chat_id = create_chat_engine(index)
    else:
        chat_id = None

    return {"transcription_id": str(inserted_id), "chat_id": chat_id, "summary": query_result.response, "transcription": transcription, "fileUrl": fileUrl}


@app.post("/create_chat")
async def create_chat(transcript_id: str):

    if not transcript_id:
        raise HTTPException(status_code=400, detail="transcript_id is required")
    transcription = transcript_collection.find_one(ObjectId(transcript_id))
    if not transcription:
        raise HTTPException(status_code=404, detail="Transcript not found")

    transcription["_id"] = str(transcription["_id"])

    index = create_index_and_query(transcript_id, transcription["transcription"])
    
    chat_id = create_chat_engine(index)

    return {"chat_id": chat_id, "transcript_id": transcript_id}


@app.post('/history_chat')
async def history_chat(payload: Agent2QuestionRequest):
    global chat_engines

    if not payload.chat_id:
        raise HTTPException(status_code=400, detail="Chat ID is required")

    # Check if the chat engine is already loaded
    if payload.chat_id not in chat_engines:
        return 'Chat not found'
    
    response = chat_engines[payload.chat_id].chat(payload.question)

    return response
