import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import os
from chromadb.utils import embedding_functions
from vector_utils import similiarty_search, get_all_memories
from typing import List
from llm_utils import get_embedding, call_llm
from scipy.spatial.distance import cosine
from config import RETRIEVAL_WEIGHTS
import datetime
from environment_objects import Building, Room
from memory import Memory
import json
from config import IMPORTANCE_PROMPT, INITIAL_PLAN_PROMPT, PLAN_PROMPT_DAY, PLAN_PROMPT_BLOCK, ACTION_LOCATION_PROMPT, RETRIEVAL_WEIGHTS, PLAN_REACTION_PROMPT
import pickle
from utils import load_pickle_environment

environment = load_pickle_environment()

for _,v in environment.agents.items():
    print(vars(v))

