from clients.groq import GroqClient
import os
import requests

from client import OpenAIClient
from settings import AGENT_KEY

groq_client = GroqClient()

folder_path = "przesłuchania"
folder_path_txt = "przesłuchania_txt"


hearings = {}
for filename in os.listdir(folder_path):
    print("Przygotowuję transkrypcję dla pliku", filename)
    name = filename.split(".")[0]
    transcription = groq_client.transcript_from_audio(
        os.path.join(folder_path, filename)
    )
    hearings[name] = transcription

for name, transcription in hearings.items():
    with open(f"{name}.txt", "a") as f:
        f.write(transcription)
hearings = {}
for filename in os.listdir(folder_path_txt):
    with open(os.path.join(folder_path_txt, filename), "r") as f:
        file_name = filename.split(".")[0]
        content = f.read()
        hearings[file_name] = content

print(hearings)

prompt = f"""
Poniżej przekażę ci przesłuchania 6 osób. Twoim zadaniem jest przeanalizowanie każdego z nich i odpowiedzenie na pytanie:
\"na jakiej ulicy znajduje się uczelnia, na której wykłada Andrzej Maj?\"
W transkrypcjach nie ma jednoznacznej odpowiedzi, sa jedynie podpowiedzi. Musisz użyć swojej własnej wiedzy, aby odpowiedzieć na pytanie.

Pamiętaj, że zeznania świadków mogą być sprzeczne, niektórzy z nich mogą się mylić, a inni odpowiadać w dość dziwaczny sposób.

Transkrypcje jako pythonowy słownik, gdzie klucz to imię przesłuchiwanego, a wartość to jego przesłuchania: {hearings}

Podaj nam proszę nazwę ulicy, na której znajduje się uczelnia (konkretny instytut!), gdzie wykłada profesor.
"""


messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt},
]
print("Wysyłam request do OpenAI API")
open_ai_client = OpenAIClient("gpt-4o")
response = open_ai_client.get_response(messages, max_tokens=2000)
result = open_ai_client.get_response_content(response)
print(result)


answer_data = {"task": "mp3", "apikey": AGENT_KEY, "answer": "Łojasiewicza"}

response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())
