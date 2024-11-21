from clients.openai import OpenAIClient
import os
import requests
from settings import AGENT_KEY
from zadania.zadanie_11.prompts import NOTES_PROMPT, SYSTEM_PROMPT, FACTS_PROMPT
from zadania.zadanie_11.prompts_2 import ABOUT_WHO_PROMPT

open_ai = OpenAIClient(model="gpt-4o")

FILES_DIRECTORY = "pliki_z_fabryki"
FACTS_DIRECTORY = "pliki_z_fabryki/facts"

system_message = open_ai.prepare_message(SYSTEM_PROMPT, role="system")

about_who = {}

for file_name in os.listdir(FACTS_DIRECTORY):
    if not file_name.endswith(".txt"):
        continue
    file_path = os.path.join(FACTS_DIRECTORY, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    if "entry deleted" in content:
        continue
    fact_message = open_ai.prepare_message(ABOUT_WHO_PROMPT.format(note=content))
    response = open_ai.chat([fact_message])
    result = open_ai.get_content(response)
    about_who[result] = content
print(about_who.keys())


answer = {}
# facts_message = open_ai.prepare_message(FACTS_PROMPT.format(note=facts_all))


for file_name in os.listdir(FILES_DIRECTORY):
    if file_name.endswith("txt"):
        file_path = os.path.join(FILES_DIRECTORY, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        about_who_prompt = ABOUT_WHO_PROMPT.format(note=content)
        about_who_message = open_ai.prepare_message(about_who_prompt)
        about_who_response = open_ai.chat([about_who_message])
        about_who_result = open_ai.get_content(about_who_response)
        print(about_who_result)
        # print(about_who_result)
        fact_content = about_who.get(about_who_result, "")
        if fact_content:
            print(file_name, "----", about_who_result)
            content += fact_content
        prompt = NOTES_PROMPT.format(note=content, file_name=file_name)
        message = open_ai.prepare_message(prompt)
        messages_to_ai = [system_message, message]
        response = open_ai.chat(messages_to_ai)
        result = open_ai.get_content(response)
        # # tags = [s for s in result.split(', ')]
        answer[file_name] = result.strip()


print(answer)

answer_data = {"task": "dokumenty", "apikey": AGENT_KEY, "answer": answer}
response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())
