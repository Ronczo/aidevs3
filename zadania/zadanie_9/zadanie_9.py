import requests
import base64
import os

from clients.groq import GroqClient
from clients.openai import OpenAIClient

map_directory = "pliki_z_fabryki/"
open_ai = OpenAIClient(model="gpt-4o")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


result_dict = {
    "people": [],
    "hardware": [],
}

# prompt_image = """
# I sent you image. Check it carefully and tell me what it is about. If it's about people, write 'people', if it's about hardware, write 'hardware'. If its about something else, write 'other'.
# By hardware I mean fixing hardware issues. By people I mean information about captured people or their traces of presence
# """
#
# txt_prompt = """
# I will send you a note. You job is to read it, analyze and tell me what it is about. If it's about people, write 'people', if it's about hardware, write 'hardware'. If its about something else, write 'other'.
# By hardware I mean fixing hardware issues. By people I mean information about captured people or their traces of presence
# """


prompt_image = """
Wysyłam Ci zdjęcie. Przenalizuj jego treść i określ o czym to jest.
Wydobądź  proszę  notatki zawierające informacje o schwytanych ludziach lub o śladach 
ich obecności (i nadaj im kategorię 'people') oraz o naprawionych usterkach hardwarowych (pomiń te związane z softem) (i nadaj im kategorię 'hardware').
Moze być tak, że treść nie pasuje do żadnej z kategorii. Wtedy nadaj kategorię 'other'.
Chcę abyś odpowiedzial jednym słowem - kategorią
Bądź krytyczny w swoim osądzie.
"""

txt_prompt = """
Wyślę ci notatkę (raport). Twoim zadaniem jest przeczytanie jej, przeanalizowanie i określenie o czym jest.
Wydobądź  proszę  notatki zawierające informacje o schwytanych ludziach lub o śladach 
ich obecności (i nadaj im kategorię 'people') oraz o naprawionych usterkach hardwarowych (pomiń te związane z softem) (i nadaj im kategorię 'hardware').
Moze być tak, że treść nie pasuje do żadnej z kategorii. Wtedy nadaj kategorię 'other'.
Chcę abyś odpowiedzial jednym słowem - kategorią
Bądź krytyczny w swoim osądzie.
"""

for map_file in os.listdir(map_directory):
    if map_file.endswith(".png"):
        file = os.path.join(map_directory, map_file)
        encoded_image = encode_image(file)
        image_url = f"data:image/jpeg;base64,{encoded_image}"
        message = open_ai.prepare_message_with_image_url(image_url, prompt_image)
        respone = open_ai.chat([message])
        result_png = open_ai.get_content(respone)
        print(result_png)
        category = result_dict.get(result_png, None)
        if category is not None:
            category.append(map_file)
        continue
    if map_file.endswith(".txt"):
        with open(os.path.join(map_directory, map_file), "r") as f:
            content = f.read()
            system_message = open_ai.prepare_message(txt_prompt, role="system")
            message = open_ai.prepare_message(content)
            response = open_ai.chat([system_message, message])
            result_txt = open_ai.get_content(response)
            print(result_txt)
            category = result_dict.get(result_txt, None)
            if category is not None:
                category.append(map_file)
    elif map_file.endswith(".mp3"):
        groq = GroqClient()
        content = groq.transcript_from_audio(os.path.join(map_directory, map_file))
        system_message = open_ai.prepare_message(txt_prompt, role="system")
        message = open_ai.prepare_message(content)
        response = open_ai.chat([system_message, message])
        result_mp3 = open_ai.get_content(response)
        print(result_mp3)
        category = result_dict.get(result_mp3, None)
        if category is not None:
            category.append(map_file)


print(result_dict)
from conf import AGENT_KEY


result_dict["people"] = sorted(result_dict["people"])
result_dict["hardware"] = sorted(result_dict["hardware"])

answer_data = {"task": "kategorie", "apikey": AGENT_KEY, "answer": result_dict}

response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())


accepted_result = {
    "people": [
        "2024-11-12_report-00-sektor_C4.txt",
        "2024-11-12_report-10-sektor-C1.mp3",
        "2024-11-12_report-07-sektor_C4.txt",
    ],
    "hardware": [
        "2024-11-12_report-13.png",
        "2024-11-12_report-15.png",
        "2024-11-12_report-17.png",
    ],
}
