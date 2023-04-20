from memory import Memory
from language_model import ask_question, generate_text
from world_operations import world_to_natural_language, find_elements_of_type
import numpy as np
from scipy.spatial.distance import cosine
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
nltk.download('stopwords')

class Agent:
    def __init__(self, name: str, description: str, world: dict):
        self.name = name
        self.memory_stream = [Memory(description)]
        self.world = world
        self.location = world["buildings"][0]

    def move(self, destination):
        # Move the agent to the destination
        if destination in find_elements_of_type(self.world, "Building"):
            self.location = destination
            return True
        else:
            return False

    def add_memory(self, description: str):
        self.memory_stream.append(Memory(description))

    def retrieve_memories(self, query, k=5):
        stop_words = set(stopwords.words('english'))
        query_tokens = [w for w in word_tokenize(query) if w not in stop_words]

        def relevance_score(memory):
            memory_tokens = [w for w in word_tokenize(memory.description) if w not in stop_words]
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([' '.join(query_tokens), ' '.join(memory_tokens)])
            if tfidf_matrix.shape[1] == 0:
                return 0
            query_vector = tfidf_matrix[0].toarray().flatten()
            memory_vector = tfidf_matrix[1].toarray().flatten()
            if not np.any(query_vector) or not np.any(memory_vector):
                return 0
            return 1 - cosine(query_vector, memory_vector)

        scored_memories = [(memory, relevance_score(memory)) for memory in self.memory_stream]
        scored_memories.sort(key=lambda x: x[1], reverse=True)

        return [mem[0] for mem in scored_memories[:k]]

    def create_reflection(self):
        recent_memories = self.retrieve_memories("", k=5)
        text = " ".join([str(memory) for memory in recent_memories])
        question = "What can I learn from these experiences?"
        reflection = ask_question(question, text)
        self.add_memory(reflection)
        return reflection

    def create_plan(self):
        current_location_description = world_to_natural_language(self.location)
        question = f"What should I do at {current_location_description}?"
        plan = ask_question(question, "")
        self.add_memory(plan)
        return plan

    def generate_dialogue(self, other_agent):
        question = f"What should I talk about with {other_agent.name}?"
        topic = ask_question(question, "")
        conversation = generate_text(topic)
        return conversation

    def __str__(self):
        return self.name
