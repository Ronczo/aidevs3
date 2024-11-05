from conf import API_KEY as OPEN_AI_API_KEY, OPEN_AI_API_URL
import requests


class OpenAIClient:
    API_KEY = OPEN_AI_API_KEY
    API_URL = OPEN_AI_API_URL
    OPEN_AI_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    def __init__(self, model, messages, max_tokens=100):
        self.model = model
        self.messages = messages
        self.max_tokens = max_tokens

    def get_response(self):
        data = {
            "model": self.model,
            "messages": self.messages,
            "max_tokens": self.max_tokens,
        }
        response = requests.post(self.API_URL, headers=self.OPEN_AI_HEADERS, json=data)
        return response

    def model_setter(self, model):
        self.model = model

    def messages_setter(self, messages):
        self.messages = messages

    def max_tokens_setter(self, max_tokens):
        self.max_tokens = max_tokens
