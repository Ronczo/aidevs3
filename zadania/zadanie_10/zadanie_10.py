import ast
import base64
import json

import requests

from clients.groq import GroqClient
from clients.openai import OpenAIClient
from settings import AGENT_KEY
from bs4 import BeautifulSoup
import os

from zadania.zadanie_10.prompts import IMG_PROMPT_10, MP3_PROMPT_10, CONTENT_PROMPT_10, GENERAL_PROMPT_10


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def download_mp3_file(parsed_content):
    audio_tag = parsed_content.find('audio')
    if audio_tag:
        source_tag = audio_tag.find('source')
        if source_tag and 'src' in source_tag.attrs:
            mp3_url = source_tag['src']
            mp3_url = f"https://centrala.ag3nts.org/dane/{mp3_url}"
            response = requests.get(mp3_url, stream=True)
            if response.status_code == 200:
                with open('files/downloaded_file.mp3', 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                print("Plik został pobrany i zapisany jako 'downloaded_file.mp3'")
                return "downloaded_file.mp3"
        else:
            return None

def download_images(soup):
    images_with_description = {}
    figures = soup.find_all("figure")
    for i, figure in enumerate(figures, start=1):
        description = figure.find("figcaption").text
        img_src = figure.find("img")['src']
        url = f"https://centrala.ag3nts.org/dane/{img_src}"
        img_response = requests.get(url)
        img_path = os.path.join("", f"{i}.jpg")
        with open(f"files/{img_path}", 'wb') as file:
            file.write(img_response.content)
        images_with_description[img_path] = description
        print(f"Pobrano: {img_path}")
    return images_with_description

groq_client = GroqClient()
open_ai = OpenAIClient(model="gpt-4o")
ARTICLE_URL = 'https://centrala.ag3nts.org/dane/arxiv-draft.html'
FILES_DIRECTORY = 'files'
QUESTIONS_URL = f"https://centrala.ag3nts.org/data/{AGENT_KEY}/arxiv.txt"
questions_dict = {}
questions = requests.get(QUESTIONS_URL).content.decode('utf-8')

article = requests.get(ARTICLE_URL).content.decode('utf-8')
soup = BeautifulSoup(article, 'html.parser')
download_mp3_file(soup)
images = download_images(soup)
container = soup.find("div", class_="container")
for figure in container.find_all("figure"):
    figure.decompose()
content = container.get_text(separator="\n", strip=True)

files_messages = []

for file in os.listdir(FILES_DIRECTORY):
    if file.endswith(".mp3"):
        print(file)
        print("groq transciption starts")
        transcription = groq_client.transcript_from_audio(
            os.path.join(FILES_DIRECTORY, file)
        )
        prompt = MP3_PROMPT_10.format(transcription=transcription)
        message = open_ai.prepare_message(prompt, role="user")
        message = files_messages.append(message)
        print("groq ends")
    elif file.endswith(".jpg"):
        print("image starts")
        description = images.get(file)
        image_prompt = IMG_PROMPT_10.format(description=description)
        message = open_ai.prepare_message_with_image_url(
            f"data:image/jpeg;base64,{encode_image(os.path.join(FILES_DIRECTORY, file))}", image_prompt, role="user"
        )
        files_messages.append(message)

prompt_content = CONTENT_PROMPT_10.format(content=content)
content_message = open_ai.prepare_message(prompt_content, role="user")
files_messages.append(content_message)





for q in questions.split('\n'):
    if q:
        id_, question = q.split('=')
        questions_dict[id_.strip()] = question.strip()


general_prompt = GENERAL_PROMPT_10.format(questions=questions_dict)
print(general_prompt)

general_message = open_ai.prepare_message(general_prompt, role="system")

print("Wysyłam request do OpenAI API")
response = open_ai.chat([*files_messages, content_message, general_message])
result = open_ai.get_content(response)
result_answer = ast.literal_eval(result)
print(result_answer)

answer_data = {"task": "arxiv", "apikey": AGENT_KEY, "answer": result_answer}
response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())