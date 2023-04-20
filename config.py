from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
SERVER_PORT = 8000
MAX_AGENTS = 10
