import requests

from clients.openai import OpenAIClient
from clients.qdrant import QdrantClient
from settings import AGENT_KEY
import os
from qdrant_client.http.models import VectorParams
from zadania.zadanie_12.prompts import TAG_PROMPT, TAG_SYSTEM_PROMPT, DATE_PROMPT


FILES_DIRECTORY = "pliki/"
qdrant = QdrantClient()
open_ai = OpenAIClient(model="gpt-4o", embedding_model="text-embedding-3-large")


# collection_name = qdrant.collection
#

# vector_size = 3072
# distance_metric = "Cosine"

#
# # Tworzenie kolekcji
# r = qdrant.client.create_collection(
#     collection_name=collection_name,
#     vectors_config=VectorParams(size=vector_size, distance=distance_metric)
# )
# print(r)

# for file_name in os.listdir(FILES_DIRECTORY):
#     file_path = os.path.join(FILES_DIRECTORY, file_name)
#     with open(file_path, "r", encoding="utf-8") as file:
#         content = file.read()
#     vector_response = open_ai.generate_embedding(content)
#     vector = open_ai.get_vector_from_embedding(vector_response)
#     tags_prompt = TAG_PROMPT.format(content=content)
#     tag_system_message = open_ai.prepare_message(TAG_SYSTEM_PROMPT, role="system")
#     message = open_ai.prepare_message(tags_prompt)
#     tag_response = open_ai.chat([tag_system_message, message])
#     tag_result = open_ai.get_content(tag_response)
#     tags = [s for s in tag_result.split(", ")]
#     vector_meta_data = {
#         "tags": tags,
#         "file_name": file_name,
#         "date": file_name.replace("_", "-").replace(".txt", ""),
#     }
#     qdrant.add_embedding(vector, vector_meta_data)

QUESTION = "W raporcie, z którego dnia znajduje się wzmianka o kradzieży prototypu broni?"
question_response = open_ai.generate_embedding(QUESTION)
question_vector = open_ai.get_vector_from_embedding(question_response)
result = qdrant.search_results(question_vector, limit=1)
answer = result[0].payload['date']
print(result)
answer_data = {"task": "wektory", "apikey": AGENT_KEY, "answer": answer}
response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())
