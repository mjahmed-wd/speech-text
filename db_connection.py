import pymongo
import os

# from pymongo import MongoClient

# # Assuming you have a MongoDB connection, replace 'your_database' and 'your_collection' with your actual database and collection names
# client = MongoClient('mongodb://localhost:27017')
# database = client['speech-to-text']
# collection = database['transcripts']

# Example 1: Insert a single document
# dictionary2 = {'Name': 'Harry2', 'Marks': 150}
# collection.insert_one(dictionary2)

def connect_to_mongodb():
    
    # Get MongoDB connection details from environment variables
    mongo_host = os.environ.get("MONGO_HOST")
    mongo_port = os.environ.get("MONGO_PORT")
    mongo_database = os.environ.get("MONGO_DATABASE")
    transcript_collection_name = os.environ.get("MONGO_COLLECTION_TRANSCRIPT")
    chat_collection_name = os.environ.get("MONGO_COLLECTION_CHAT")
    # mongo_uri = os.environ.get("MONGO_URI")
    mongo_uri = 'mongodb://mongo-primary:27017'

    client = pymongo.MongoClient(f"{mongo_uri}")

    db = client[mongo_database]

    transcript_collection = db[transcript_collection_name]
    chat_collection = db[chat_collection_name]

    # transcript_collection.insert_one({"fileUrl": "test", "transcription": "test"})

    print(f"Connected to MongoDB")


    # Perform operations on the collection
    # ...

    # Close the connection
    # client.close()

    return (db, transcript_collection, chat_collection)
