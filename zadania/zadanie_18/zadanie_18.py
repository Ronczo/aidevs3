import ast

from clients.openai import OpenAIClient
from clients.scrapy import ScrapyClient
from settings import AGENT_KEY
import requests

from zadania.zadanie_18.prompts import QUESTION_PROMPT

QUESTIONS_URL = f"https://centrala.ag3nts.org/data/{AGENT_KEY}/softo.json"
SOFTO_URL = 'https://softo.ag3nts.org'
scrapy_client = ScrapyClient()

open_ai = OpenAIClient(model="gpt-4o", embedding_model="text-embedding-3-large")
questions_response = requests.get(QUESTIONS_URL)
questions = questions_response.json()
questions_str = " ".join(
    [f"{k}: {v}" for k, v in questions.items()]
)

answers = {
    id_: "NO" for id_ in questions.keys()
}
scrapy_client.run_spider("softo_spider")
# whole_content = " ".join(scrapy_client.results)
for item in scrapy_client.results:
    content = item['text']
    content_prompt = QUESTION_PROMPT.format(text=content, questions=questions_str)
    content_message = open_ai.prepare_message(content_prompt)
    response = open_ai.chat([content_message])
    response_content = open_ai.get_content(response)
    if not response_content == "NO":
        try:
            response_dict = ast.literal_eval(response_content)
            for k, v in response_dict.items():
                if answers[k] == "NO":
                    answers[k] = v
        except:
            print("Error")
            print(response_content)

answer_data = {"task": "softo", "apikey": AGENT_KEY, "answer": answers}
response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())

