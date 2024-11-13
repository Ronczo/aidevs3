import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
AGENT_KEY = os.getenv("AGENT_KEY")
OPEN_AI_API_URL = "https://api.openai.com/v1/chat/completions"
OPEN_AI_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}
