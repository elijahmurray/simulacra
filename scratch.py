from dotenv import load_dotenv
import os

# SET UP OPENAI AND THE VECTORDB CLIENT AND COLLECTION
load_dotenv()
x = os.getenv('OPEN_AI_API_KEY')
print(x)
