import requests
from bs4 import BeautifulSoup

from client import OpenAIClient

LOGIN = "tester"
PASSWORD = "574e112a"
URL = "https://xyz.ag3nts.org/"

website_response = requests.get(URL)
content = website_response.content
content_str = content.decode("utf-8")
soup = BeautifulSoup(content_str, "html.parser")
p_element = soup.find("p", id="human-question")
question = p_element.get_text().removeprefix("Question:")
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {
        "role": "user",
        "content": f"There is my question in Polish: {question}. Answer it as number",
    },
]

client = OpenAIClient("gpt-4o-mini", messages)
response = client.get_response()
answer_year = response.json()["choices"][0]["message"]["content"]
login_response = requests.post(
    URL,
    data={"username": LOGIN, "password": PASSWORD, "answer": answer_year},
)

print(login_response.content)
