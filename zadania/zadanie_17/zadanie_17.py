import json

from clients.openai import OpenAIClient
from settings import AGENT_KEY
import requests

FILES_DIR = 'lab_data'

open_ai = OpenAIClient(model="gpt-4o-mini", embedding_model="text-embedding-3-large")


jsons = []

SYSTEM_MESSAGE = "Evaluate the research results"
system_message = open_ai.prepare_message(SYSTEM_MESSAGE, role="system")

with open(f'{FILES_DIR}/correct.txt', 'r') as f:
    for line in f:
        content = line.strip()
        content_message = open_ai.prepare_message(content)
        assistant_message = open_ai.prepare_message("correct", role="assistant")
        messages = {
            "messages": [system_message, content_message, assistant_message]
        }
        jsons.append(messages)


with open(f'{FILES_DIR}/incorrect.txt', 'r') as f:
    for line in f:
        content = line.strip()
        content_message = open_ai.prepare_message(content)
        assistant_message = open_ai.prepare_message("incorrect", role="assistant")
        messages = {
            "messages": [system_message, content_message, assistant_message]
        }
        jsons.append(messages)

# file for fine-tuning
with open('dane.jsonl', 'w') as plik:
    for row in jsons:
        json.dump(row, plik)
        plik.write('\n')


open_ai = OpenAIClient(model="ft:gpt-4o-mini-2024-07-18:personal:ai-dev3-labs17:AZhwyLbP", embedding_model="text-embedding-3-large")


answer = []
with open(f'{FILES_DIR}/verify.txt', 'r') as f:
    for line in f:
        id_, content = line.split("=")
        print(id_, content)
        content_message = open_ai.prepare_message(content)
        messages = [system_message, content_message]
        response = open_ai.chat(messages)
        response_content = open_ai.get_content(response)
        if response_content == "correct":
            answer.append(id_)
# answer_messages = [system_message]

answer_data = {"task": "research", "apikey": AGENT_KEY, "answer": answer}
response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())



