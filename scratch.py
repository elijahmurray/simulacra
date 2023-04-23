import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import os
from chromadb.utils import embedding_functions

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


records = collection.get(
    where={"agent": "Truman Burbank"},
    #include=["documents"]
)

print(collection.peek()["embeddings"])
