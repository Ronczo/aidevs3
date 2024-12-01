import ast
from unidecode import unidecode
import requests
import os

from clients.openai import OpenAIClient
from settings import AGENT_KEY
from zadania.zadanie_14.prompts import BARBARA_PROMPT, ANSWER_PROMPT

PEOPLE_API_URL = "https://centrala.ag3nts.org/people"
PLACES_API_URL = "https://centrala.ag3nts.org/places"
BARBARA_TXT_URL = "https://centrala.ag3nts.org/dane/barbara.txt"

open_ai = OpenAIClient(model="gpt-4o", embedding_model="text-embedding-3-large")
barbara_txt = requests.get(BARBARA_TXT_URL)
barbara_content = barbara_txt.text
barbara_prompt = BARBARA_PROMPT.format(note=barbara_content)
barbara_message = open_ai.prepare_message(barbara_prompt)
barbara_response = open_ai.chat([barbara_message])
barbara_result = open_ai.get_content(barbara_response)

barbara_dict = ast.literal_eval(barbara_result)
people_all = [p.upper() for p in barbara_dict["people"]]
places_all = [p.upper() for p in barbara_dict["places"]]
print(barbara_dict)
result = {}
keys = 0
values = 0
new_keys = 1
new_values = 1
while keys != new_keys or values != new_values:
    keys = new_keys
    values = new_values
    for person in people_all:
        data = {"apikey": AGENT_KEY, "query": unidecode(person)}
        response = requests.post(PEOPLE_API_URL, json=data)
        if response.status_code != 200:
            print("PEROSN", data)
        cities_str = response.json()['message']
        if "RESTRICTED" in cities_str or "centrala.ag3nts.org" in cities_str.lower():
            result[unidecode(person.upper())] = result.get(unidecode(person.upper()), [])
            continue
        cities = cities_str.split(" ")
        result[unidecode(person.upper())] = list(set(cities))


    for place in places_all:
        data = {"apikey": AGENT_KEY, "query": unidecode(place)}
        response = requests.post(PLACES_API_URL, json=data)
        if response.status_code != 200:

            print("PLACE", data)
        names_str = response.json()['message']
        if "RESTRICTED" in names_str or "centrala.ag3nts.org" in names_str.lower():
            continue
        names = names_str.split(" ")
        for name in names:
            places_list = result.get(unidecode(name.upper()), [])
            places_list.append(unidecode(place.upper()))
            places_list = list(set(places_list))
            result[unidecode(name.upper())] = places_list


    new_keys = len(result.keys())
    people_all = [p for p in result.keys()]

    value_set = set()
    for l in result.values():
        for c in l:
            value_set.add(c)
    places_all = list(value_set)
    new_values = len(value_set)
    print(result)

answer_prompt = ANSWER_PROMPT.format(note=barbara_content, cities=", ".join(result[unidecode("barbara".upper())]))
answer_message = open_ai.prepare_message(answer_prompt)
answer_response = open_ai.chat([answer_message])
answer = open_ai.get_content(answer_response)
print(answer)

answer_data = {"task": "loop", "apikey": AGENT_KEY, "answer": "ELBLAG"}
response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())
