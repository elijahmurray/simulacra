import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import os

# SET UP OPENAI AND THE VECTORDB CLIENT AND COLLECTION

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="vectordb"
))

try:
  collection = client.get_collection(name='memories')
except ValueError as e:
  print("No collection found")


records = collection.get(
    where={"agent": "Truman Burbank"},
    include=["documents"]
)

for record in records['documents']:
  print(record)
