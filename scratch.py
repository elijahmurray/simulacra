import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import os
from chromadb.utils import embedding_functions
from vector_utils import similiarty_search, get_all_memories
from typing import List
from llm_utils import get_embedding
from scipy.spatial.distance import cosine
from config import RETRIEVAL_WEIGHTS
import datetime
'''

# SET UP OPENAI AND THE VECTORDB CLIENT AND COLLECTION
load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
  api_key=OPEN_AI_API_KEY,
  model_name="text-embedding-ada-002"
)

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="vectordb"
))

try:
  collection = client.get_collection(name='memories', embedding_function=openai_ef)
except ValueError as e:
  print("No collection found")

results = get_all_memories("Truman Burbank")
print(results)


records = collection.get(
    where={"agent": "Truman Burbank"},
    include=["documents", "embeddings", "metadatas"]
)

query = "what are the objects in Truman's bedroom Truman can interact with?"
result = similiarty_search("Truman Burbank", query, 2)

print("Records:")
for document in records["documents"]:
  print(document)

print("Results:")
for document in result["documents"][0]:
  print(document)

'''
sim_time = datetime.datetime.now()
def retrieve_memory(agent_name, query: str, n: int = 3):
        # Get all memories for agent
        memories = get_all_memories(agent_name)
        query_embedding = get_embedding(query)

        def calculate_relevance_score(memory_embedding: List, query_embedding: List) -> float:
            return cosine(query_embedding, memory_embedding)

        def calculate_recency_score(last_accessed: datetime.datetime) -> float:
            hours_since_accessed = (sim_time - last_accessed).total_seconds() / 3600
            decay_factor = 0.99
            recency_score = decay_factor ** hours_since_accessed
            return recency_score

        def score_memory(memory_dict: dict) -> float:
            relevance_score = calculate_relevance_score(memory_dict["embedding"], query_embedding)
            recency_score = calculate_recency_score(memory_dict["last_accessed"])
            importance_score = memory_dict["importance_score"]
            final_score = (relevance_score * RETRIEVAL_WEIGHTS["relevance"]) + (float(importance_score)* RETRIEVAL_WEIGHTS["importance"]) + (recency_score * RETRIEVAL_WEIGHTS["recency"])
            return final_score

        for memory in memories:
            memory["score"] = score_memory(memory)

        sorted_memories = sorted(memories, key=lambda k: k["score"], reverse=False)

        for m in sorted_memories:
            print(f"{m['score']}: {m['description']}")

        return sorted_memories[:n]

top_mem = retrieve_memory("Truman Burbank", "What does Truman like to do for fun?")

for mem in top_mem:
     print(mem["description"])
