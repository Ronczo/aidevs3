from ai_agent.clients.openai import OpenAIClient
from conf import AGENT_KEY
import requests


ROBOT_DESCRIPTION_URL = f"https://centrala.ag3nts.org/data/{AGENT_KEY}/robotid.json"
robot_description = requests.get(ROBOT_DESCRIPTION_URL).json()["description"]


open_ai = OpenAIClient(model="dall-e-3")
result = open_ai.generate_image_response(robot_description)
picture_url = open_ai.get_url_of_generated_image(result)
print(picture_url)
answer_data = {"task": "robotid", "apikey": AGENT_KEY, "answer": picture_url}

response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())
