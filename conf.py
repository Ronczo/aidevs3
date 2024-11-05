import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPEN_AI_API_KEY")
OPEN_AI_API_URL = "https://api.openai.com/v1/chat/completions"
OPEN_AI_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}
