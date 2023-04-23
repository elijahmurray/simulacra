from llm_utils import get_embedding
from typing import List
from memory import Memory
import uuid
import openai
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import os

# SET UP OPENAI AND THE VECTORDB CLIENT AND COLLECTION
load_dotenv()
openai.api_key = os.getenv("OPEN_AI_API_KEY")

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="vectordb"
))

try:
  #collection = client.get_collection(name='memories')
  client.delete_collection(name="memories")
  collection = client.create_collection(name='memories')
except ValueError as e:
  collection = client.create_collection(name='memories')


def get_memory_embedding(memory: Memory) -> List:
    '''
    Creates an embedding for a given text string using OpenAI's embedding API endpoint.
    '''
    response = openai.Embedding.create(
        input=memory.description,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

def store_memory_in_vectordb(agent_name: str, memory: Memory) -> None:
    '''
    Stores an embedding (consisting of text plus an embedding vector) in a database, and sets metadata.
    '''
    embedding = get_memory_embedding(memory)
    collection.add(
       documents=[memory.description],
       embeddings = [embedding],
       metadatas=[{"agent": agent_name, "created_at": str(memory.created_at), "last_accessed": str(memory.last_accessed), "importance_score": memory.importance_score}],
       ids=[str(uuid.uuid4())]
    )

def similiarty_search(query: str) -> List:
    pass
