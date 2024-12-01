from datetime import datetime

import requests

from clients.openai import OpenAIClient
from conf import AGENT_KEY
from zadania.zadanie_16.prompts import REPAIR_CHOOSING_PROMPT, GETTING_URLS_PROMPT, CORRECT_URL_PROMPT_SYSTEM, \
    CORRECT_URL_PROMPT

open_ai = OpenAIClient(model="gpt-4o", embedding_model="text-embedding-3-large")

start_data = {"task": "photos", "apikey": AGENT_KEY, "answer": "START"}
start_response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=start_data,
)


def get_urls_from_text(text):
    urls_prompt = GETTING_URLS_PROMPT.format(note=text)
    urls_message = open_ai.prepare_message(urls_prompt)
    urls_response = open_ai.chat([urls_message])
    urls_result = open_ai.get_content(urls_response)
    return [s for s in urls_result.split(",") if s]


def choose_repair_option(url):
    repair_prompt = REPAIR_CHOOSING_PROMPT
    repair_message = open_ai.prepare_message_with_image_url(url, repair_prompt)
    repair_response = open_ai.chat([repair_message])
    repair_result = open_ai.get_content(repair_response)
    return repair_result


def repair_order(url, option):
    file_name = url.split("/")[-1]
    repair_order_data = {
        "task": "photos",
        "apikey": AGENT_KEY,
        "answer": f"{option} {file_name}",
    }
    repair_order_response = requests.post(
        "https://centrala.ag3nts.org/report",
        json=repair_order_data,
    )
    return repair_order_response.json()["message"]


CORRECTED_URLS = {}


def judge_urls(urls):
    urls_copy = urls.copy()
    for url in urls:
        urls_copy.remove(url)
        option = choose_repair_option(url)
        if option == "OK":
            CORRECTED_URLS[url] = option
        else:
            new_url = repair_order(url, option)
            new_url = get_urls_from_text(new_url)
            urls_copy.extend(new_url)
    if urls:
        print(urls)
        judge_urls(urls_copy)


# urls = get_urls_from_text(start_response.json()['message'])
# judge_urls(urls)

# Code above gave me this result
MOCKED_CORRECT_URL = {
    "https://centrala.ag3nts.org/dane/barbara/IMG_1444.PNG": "OK",
    "https://centrala.ag3nts.org/dane/barbara/IMG_1410_FXER.PNG": "OK",
    "https://centrala.ag3nts.org/dane/barbara/IMG_1443_FT12.PNG": "OK",
    "https://centrala.ag3nts.org/dane/barbara/IMG_559_NRR7.PNG": "OK",
}

system_prompt = CORRECT_URL_PROMPT_SYSTEM
system_message = open_ai.prepare_message(system_prompt, role="system")
url_messages = []
for url in MOCKED_CORRECT_URL:
    correct_url_prompt = CORRECT_URL_PROMPT
    message = open_ai.prepare_message_with_image_url(url, correct_url_prompt)
    url_messages.append(message)

response = open_ai.chat(url_messages)
response_content = open_ai.get_content(response)
print(response_content)



answer_data = {"task": "photos", "apikey": AGENT_KEY, "answer": response_content}
response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())
