import openai
import requests
from conf import API_KEY
from bs4 import BeautifulSoup

openai.api_key = API_KEY
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
        "content": f"There is my question in Polish: {question}. Answer must be a number, Ignore other words. I need a number",
    },
]
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print(response.choices[0].message.content)