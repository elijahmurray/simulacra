import pinecone

class PineconeManager:
    def __init__(self, api_key, index_name="memory_vectors", dimension=1536, environment=None):
        print("Initializing PineconeManager...")
        pinecone.init(api_key=api_key, environment=environment)
        self.pinecone = pinecone
        if index_name:
            print("Setting index_name...")
            self.set_index(index_name, dimension)
        print("PineconeManager initialized.")

    def set_index(self, index_name, dimension="1024"):
        existing_indexes = self.pinecone.list_indexes()
        if index_name not in existing_indexes and dimension:
            print(f"Creating index {index_name} with dimension {dimension}...")
            self.create_index(index_name, dimension)
        
        self.index_name = index_name
        self.index = self.pinecone.Index(index_name)

    def create_index(self, index_name, dimension, metadata_config=None):
        self.pinecone.create_index(index_name, dimension, metadata_config)

    def delete_index(self, index_name):
        self.pinecone.delete_index(index_name)
      
    def upsert(self, vectors):
        self.index.upsert(vectors=vectors)
