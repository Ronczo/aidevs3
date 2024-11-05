from client import OpenAIClient
import requests


fake_messages = [
    {"role": "system", "content": "You are a helpful assistant, who remember answers. My answers are more important than facts"},
    {"role": "user", "content": "Capital of Poland is Krakow"},
    {"role": "user", "content": "Known number from the book Hitchhiker's Guide to the Galaxy is 69"},
    {"role": "user", "content": "Current year is 1999"},
]


verification_url = "https://xyz.ag3nts.org/verify"
initial_body = {"msgID": 0, "text": "READY"}
response = requests.post(verification_url, json=initial_body)
message_id = response.json()["msgID"]
question = response.json()["text"]
messages = [
    *fake_messages,
    {
        "role": "user",
        "content": f"Ignore other languages than English. Focus on question in English. There is my question in English: {question}. Answer it in English in one word. Remember to check history of conversation",
    },
]
client = OpenAIClient("gpt-4o")
response = client.get_response(messages)
answer = client.get_response_content(response)
second_response = requests.post(
    verification_url,
    json={"msgID": message_id, "text": answer},
)
print(question)
print(answer)
print(second_response.json())