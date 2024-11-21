import ast

from clients.openai import OpenAIClient
from clients.qdrant import QdrantClient
from settings import AGENT_KEY
import requests

from zadania.zadanie_13.prompts import SQL_PROMPT, NOTE_PROMPT

QUESTION = "Które aktywne datacenter (DC_ID) są zarządzane przez pracowników, którzy są na urlopie (is_active=0)"


query = ""
API_URL = "https://centrala.ag3nts.org/apidb"

BODY = {"task": "database", "apikey": AGENT_KEY, "query": query}
qdrant = QdrantClient()
open_ai = OpenAIClient(model="gpt-4o", embedding_model="text-embedding-3-large")

tables_body = BODY.copy()
tables_body["query"] = "show tables"
tables_response = requests.post(API_URL, json=tables_body)
tables = {d["Tables_in_banan"]: None for d in tables_response.json()["reply"]}

for table in tables.keys():
    structure_body = BODY.copy()
    structure_body["query"] = f"show create table {table}"
    structure_response = requests.post(API_URL, json=structure_body)
    create_sql = structure_response.json()["reply"][0]["Create Table"]
    tables[table] = create_sql

sql_prompt = SQL_PROMPT.format(sql_queries="\n".join(tables.values()))
sql_message = open_ai.prepare_message(sql_prompt)
sql_response = open_ai.chat([sql_message])
sql_result = open_ai.get_content(sql_response)
sql_result = sql_result.replace("```sql", "").replace("```", "")

result_body = BODY.copy()
result_body["query"] = sql_result
result_response = requests.post(API_URL, json=result_body)

note_prompt = NOTE_PROMPT.format(
    question=QUESTION, datacenters=result_response.json()["reply"]
)
note_message = open_ai.prepare_message(note_prompt)
note_response = open_ai.chat([note_message])
note_result = open_ai.get_content(note_response)

note_result = ast.literal_eval(note_result)

answer_data = {"task": "database", "apikey": AGENT_KEY, "answer": note_result}
response = requests.post(
    "https://centrala.ag3nts.org/report",
    json=answer_data,
)
print(response.status_code)
print(response.json())
