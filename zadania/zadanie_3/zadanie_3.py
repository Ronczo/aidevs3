import ast
import json
import os

import requests

from client import OpenAIClient
from conf import AGENT_KEY

client = OpenAIClient("gpt-4o-mini")
file_url = f"https://centrala.ag3nts.org/data/{AGENT_KEY}/json.txt"
file_path = "json.json"

if not os.path.exists(file_path):
    file_response = response = requests.get(file_url)
    if file_response.status_code == 200:
        with open("json.json", "wb") as f:
            f.write(response.content)


with open(file_path, "r") as file:
    json_data = json.load(file)
    question_for_llm: dict = {
        q["test"]["q"]: None for q in json_data["test-data"] if "test" in q
    }
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"I have some questions for you. "
            f"I send them in python dict. Answer it in one word. "
            f"Fill my dictionary with proper answer by replacing 'None' with your answer. {question_for_llm}"
            f"Return disctionary with asnwers in the same structure",
        },
    ]
    ai_response = client.get_response(messages)
    result_ai = client.get_response_content(ai_response)
    result_ai_dict = ast.literal_eval(result_ai)
    for question in json_data["test-data"]:
        answer = question["answer"]
        calculation = question["question"].split("+")
        strip_calc = [calc.strip() for calc in calculation]
        result = int(strip_calc[0]) + int(strip_calc[1])
        if result != answer:
            question["answer"] = result
        if "test" in question:
            question_for_ai = question["test"]["q"]
            proper_answer = result_ai_dict[question_for_ai]
            question['test']['a'] = proper_answer

answer_file_path = 'answers.json'
with open(answer_file_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)


request_data = {
    "task": "JSON",
    "apikey": AGENT_KEY,
    "answer":  json_data
}


response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=request_data,
)

print(response.content)
print(response.status_code)