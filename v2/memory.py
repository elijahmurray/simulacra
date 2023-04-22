# Ripped from Matt

# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# import os
# import openai
# from dotenv import load_dotenv
# from pinecone_manager import PineconeManager

# load_dotenv()

# pinecone_manager = PineconeManager(
#     api_key=os.getenv("PINECONE_API_KEY"),
#     index_name="memory-vectors",
#     environment=os.getenv("PINECONE_ENVIRONMENT"),
# )

# openai.api_key = os.getenv("OPENAI_API_KEY")


# class MemoryObject:
#     def __init__(self, description, timestamp, importance, embedding_vector=None):
#         self.description = description
#         self.creation_timestamp = timestamp
#         self.access_timestamp = timestamp
#         self.importance = importance
#         self.embedding_vector = embedding_vector

#     @staticmethod
#     def get_importance_score(prompt, temperature=0.5):
#         model = "gpt-3.5-turbo"
#         messages = [
#             {
#                 "role": "system",
#                 "content": "You are a helpful memory analyst who will rate memory importance on a scale from 1 to 10.",
#             },
#             {
#                 "role": "user",
#                 "content": f"On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following piece of memory. Do not ask for more information, only respond with an integer score and nothing else, including no other punctuation. Memory: : {prompt} Rating: <fill in>",
#             },
#         ]
#         response = openai.ChatCompletion.create(
#             model=model, messages=messages, temperature=temperature
#         )

#         score = None
#         try:
#             message_response = response.choices[0].message["content"]
#             score = float(message_response.strip())
#             score = round(score)

#             if score < 1 or score > 10:
#                 raise ValueError(f"Invalid score value: {score}")
#         except (ValueError, KeyError, IndexError) as e:
#             print(f"Error while parsing API response: {e}")
#             score = None

#         return score


# class MemoryStream:
#     def __init__(self):
#         self.memory_stream = []
#         # these are the weights for the recency, importance, and relevance scores
#         # @todo we will need a way to tune these weights
#         self.alpha_recency = 0.25
#         self.alpha_importance = 0.5
#         self.alpha_relevance = 6
#         self.decay_factor = 0.99

#     def add_memory(self, memory):
#         self.memory_stream.append(memory)

#     def create_and_add_memory(self, description, timestamp, importance):
#         # Generate an embedding vector for the memory
#         embedding_vector = get_embeddings([description])[0]

#         # Create a new MemoryObject with the generated embedding vector
#         memory = MemoryObject(
#             description=description,
#             timestamp=timestamp,
#             importance=importance,
#             embedding_vector=embedding_vector,
#         )

#         # Add the memory to the memory stream
#         self.add_memory(memory)

#         # Store the embedding vector in Pinecone
#         memory_id = str(
#             len(self.memory_stream) - 1
#         )  # Use the index of the memory in the memory_stream as its ID
#         vectors_to_upsert = [{"id": memory_id, "values": embedding_vector}]
#         pinecone_manager.upsert(
#             vectors_to_upsert
#         )  # Pass the list of dictionaries to the upsert method

#     def retrieve_memories(self, query, current_time, top_k=1):
#         # Generate an embedding vector for the query
#         query_embedding = get_embeddings([query])[0]

#         recency_scores = []
#         importance_scores = []
#         relevance_scores = []
#         for memory in self.memory_stream:
#             # Recency score
#             hours_since_last_access = (current_time - memory.access_timestamp) / 3600
#             recency = np.exp(-self.decay_factor * hours_since_last_access)
#             recency_scores.append(recency)

#             # Importance score
#             importance_scores.append(memory.importance)

#             # Relevance score
#             relevance = cosine_similarity([memory.embedding_vector], [query_embedding])[
#                 0
#             ][0]
#             relevance_scores.append(relevance)

#             # Update access timestamp
#             memory.access_timestamp = current_time

#         # Normalize scores
#         recency_scores = recency_scores / np.linalg.norm(recency_scores, ord=2)
#         importance_scores = importance_scores / np.linalg.norm(importance_scores, ord=2)
#         relevance_scores = relevance_scores / np.linalg.norm(relevance_scores, ord=2)

#         # Calculate final scores
#         final_scores = (
#             self.alpha_recency * recency_scores
#             + self.alpha_importance * importance_scores
#             + self.alpha_relevance * relevance_scores
#         )
#         # print("All memories with individual scores:")
#         # for i, memory in enumerate(self.memory_stream):
#         #     print(f"Memory {i + 1} (Index {i}):")
#         #     print(f"Relevance Score: {relevance_scores[i]}")
#         #     print(f"Importance Score: {importance_scores[i]}")
#         #     print(f"Recency Score: {recency_scores[i]}")
#         #     print(f"Description: {memory.description}")
#         #     print(f"Total score: {final_scores[i]}")
#         #     print()

#         # Get top-k memories
#         top_indices = np.argsort(final_scores)[-top_k:]
#         top_memories = [self.memory_stream[i] for i in top_indices]

#         return top_memories


# def get_embeddings(texts):
#     embeddings = []
#     for text in texts:
#         response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
#         if "data" in response and len(response["data"]) > 0:
#             embedding = np.array(response["data"][0]["embedding"])
#             embeddings.append(embedding)
#         else:
#             raise ValueError(f"Error getting embeddings: {response}")
#     return embeddings


# # CURRENTLY A STUB AND NOT USED
# # from prompts import MEMORY_IMPORTANCE_PROMPT
# # from datetime import datetime as Datetime

# # MEMORY_TYPES = ["observation", "plan", "reflection"]


# # class Memory:
# #     def __init__(self, name, agent, description_prompt):
# #         self.name = name
# #         self.created_at = Datetime.now
# #         self.last_retrieved_at = Datetime.now
# #         self.agent = agent
# #         self.importance = self.generate_importance(self)
# #         self.description = self.description
# #         self.type = enumerate[MEMORY_TYPES]

# #     def generate_description(self, prompt):
# #         response = self.call_openai(prompt)
# #         # observation sample description: <Agent> is <active action> [preposition i.e. on/to/with] <environment object OR agent>
# #         # plan sample output description:
# #         # reflection sample output description:
# #         return response

# #     def generate_importance(self):
# #         prompt = MEMORY_IMPORTANCE_PROMPT + self.description
# #         importance = self.call_openai(prompt)
# #         return importance

# #     def call_openai(prompt):
# #         # stubbed out openAI call
# #         response = ""
# #         return response
