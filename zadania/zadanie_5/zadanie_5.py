import requests

from client import OpenAIClient
from conf import AGENT_KEY

FILE_URL = f"https://centrala.ag3nts.org/data/{AGENT_KEY}/cenzura.txt"
LOCAL_FILE_NAME = "cenzura.txt"
AI_AGENT_URL = "http://localhost:11434/api/generate"


client = OpenAIClient("gpt-4o-mini")
file_response = requests.get(FILE_URL)
if file_response.status_code == 200:
    with open(LOCAL_FILE_NAME, "wb") as f:
        f.write(file_response.content)


with open(LOCAL_FILE_NAME, "r") as file:
    content = file.read()
prompt = {
    "prompt": "Below you can find a text that needs to be censored. Please censor it."
    'You must replace all dangerous words with "CENZURA"'
    "Dangerous words are: Name and Surname (Even in Polish), city (also Polish ones),"
    " street and number (you can find street name after \"ul.\", and age (usually it's before word 'lat')"
    'Street name and number replace by one word "CENZURA"'
    'Don\'t remove words. Leave "Ulica" or similar'
    'Name and surname replace by one word "CENZURA"'
    'You can\'t change the order of words, only replace them with "CENZURA".'
    f"Text to censore: {content}"
}
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt["prompt"]},
]
print(content)
response = client.get_response(messages)
result = client.get_response_content(response)
print(result)

answer_data = {"task": "CENZURA", "apikey": AGENT_KEY, "answer": result}

response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)

print(response)
print(response.json())
