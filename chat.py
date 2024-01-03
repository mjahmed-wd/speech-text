import uuid
from llama_index import (StorageContext, VectorStoreIndex, download_loader,
                         load_index_from_storage)
from llama_index.memory import ChatMemoryBuffer



def create_index_and_query(transcript_id: str, full_transcription: any):
    persist_dir = f'./storage/cache/transcription/{transcript_id}'

    try:
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        index = load_index_from_storage(storage_context)
        print('loading from disk')
    except:
        JsonDataReader = download_loader("JsonDataReader")
        loader = JsonDataReader()
        documents = loader.load_data(full_transcription)
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=persist_dir)
        print('creating on disk')

    return index


def create_chat_engine(indexStorage: any):
    global chat_engines
    chat_id = str(uuid.uuid4()) 

    memory = ChatMemoryBuffer.from_defaults(token_limit=2000)

    chat_engine = indexStorage.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt=(
            "You are a chatbot, able to have normal interactions, as well as talk"
            # " about an essay discussing Paul Grahams life."
        ),
    )

    chat_engines[chat_id] = chat_engine

    return chat_id
