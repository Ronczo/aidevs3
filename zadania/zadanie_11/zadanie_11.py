from clients.openai import OpenAIClient
import os
import requests
from settings import AGENT_KEY
from zadania.zadanie_11.prompts import NOTES_PROMPT, SYSTEM_PROMPT, FACTS_PROMPT

open_ai = OpenAIClient(model="gpt-4o")

FILES_DIRECTORY = "pliki_z_fabryki"
FACTS_DIRECTORY = "pliki_z_fabryki/facts"

system_message = open_ai.prepare_message(SYSTEM_PROMPT, role="system")

facts_messages = []
facts_all = ""
for file_name in os.listdir(FACTS_DIRECTORY):
    if not file_name.endswith('.txt'):
        continue
    file_path = os.path.join(FACTS_DIRECTORY, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    if "entry deleted" in content:
        continue
    fact_message = open_ai.prepare_message(FACTS_PROMPT.format(fact=content))
    facts_messages.append(fact_message)
    facts_all += content


answer = {}
# facts_message = open_ai.prepare_message(FACTS_PROMPT.format(note=facts_all))


for file_name in os.listdir(FILES_DIRECTORY):
    if file_name.endswith("txt"):
        file_path = os.path.join(FILES_DIRECTORY, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        prompt = NOTES_PROMPT.format(note=content, additional=facts_all)
        message = open_ai.prepare_message(prompt)
        messages_to_ai = [system_message, message]
        response = open_ai.chat(messages_to_ai)
        result = open_ai.get_content(response)
        # tags = [s for s in result.split(', ')]
        print(result)
        answer[file_name] = result.strip()



answer_data = {"task": "dokumenty", "apikey": AGENT_KEY, "answer": answer}
response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())
