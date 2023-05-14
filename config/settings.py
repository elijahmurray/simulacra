from dotenv import load_dotenv
import os
load_dotenv()

# Used for debugging
ENABLE_PROMPT_CONTEXT_LOGGING = False  # Logs contexts to console. Generally leave off.
ENABLE_PROMPT_LOGGING = False  # Logs prompts to console. Generally leave off.
ENABLE_METHOD_CALLED_LOGGING = (
    False  # Logs names of all called methods to console. Generally leave off.
)
ENABLE_LLM_RESPONSE_LOGGING = (
    False  # Logs LLMs response to prompt to console. Generally leave off.
)
ENABLE_WORLD_EVENT_LOGGING = True  # Logs world events to console. Generally leave on.
ENABLE_AGENT_EVENT_LOGGING = True  # Logs world events to console. Generally leave on.

DEV_MODE=False

# OPENAI CONFIG
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
OPENAI_MODEL="gpt-3.5-turbo"
MAX_TOKENS=300

# MEMORY CONFIG
RETRIEVAL_WEIGHTS = {
  'importance': 1.0,
  'relevance': 0.5,
  'recency': 0.5,
}

# SIMULATION CONFIG
SIM_CLOCK_INCREMENT_MINUTES = 10
