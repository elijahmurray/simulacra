from llm_utils import get_embedding
from typing import List
from memory import Memory
import uuid
import openai
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
import json
from config import OPEN_AI_API_KEY, DEV_MODE
from utils import get_datetime_from_datetime_string

# SET UP OPENAI AND THE VECTORDB CLIENT AND COLLECTION
openai.api_key = OPEN_AI_API_KEY

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
  api_key=OPEN_AI_API_KEY,
  model_name="text-embedding-ada-002"
)

client = chromadb.Client(Settings(
  chroma_db_impl="duckdb+parquet",
  persist_directory="vectordb"
))

try:
  if DEV_MODE:
    client.delete_collection(name="memories")
    collection = client.create_collection(name='memories', embedding_function=openai_ef)
  else:
    collection = client.get_collection(name='memories', embedding_function=openai_ef)
except ValueError as e:
  collection = client.create_collection(name='memories', embedding_function=openai_ef)

def store_memory_in_vectordb(agent_name: str, memory: Memory) -> None:
  '''
  Stores an embedding (consisting of text plus an embedding vector) in a database, and sets metadata.
  '''
  collection.add(
      documents=[memory.description],
      metadatas=[{"agent": agent_name, "type": memory.type, "created_at": str(memory.created_at), "last_accessed": str(memory.last_accessed), "importance_score": memory.importance_score}],
      ids=[str(uuid.uuid4())]
  )

def similiarty_search(agent_name: str, query: str, n_results: int = 5) -> List:
  results = collection.query(
    query_texts=[query],
    n_results=n_results,
    where={"agent": agent_name}
  )
  return results

def get_all_memories(agent_name: str) -> List:
  results = collection.get(
    where={"agent": agent_name},
    include=["documents", "embeddings", "metadatas"]
  )
  memories = []
  for i in range(0,(len(results["documents"])-1)):
    memories.append(
      {
        "description": json.loads(results["documents"][i]) if "plan" in results["metadatas"][i]["type"] else results["documents"][i],
        "type": results["metadatas"][i]["type"],
        "created_at": get_datetime_from_datetime_string(results["metadatas"][i]["created_at"]),
        "last_accessed": get_datetime_from_datetime_string(results["metadatas"][i]["last_accessed"]),
        "importance_score": results["metadatas"][i]["importance_score"],
        "embedding": results["embeddings"][i]
      }
    )
  return memories
