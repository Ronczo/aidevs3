from conf import API_KEY as OPEN_AI_API_KEY, OPEN_AI_API_URL
import requests


class OpenAIClient:
    API_KEY = OPEN_AI_API_KEY
    API_URL = OPEN_AI_API_URL
    OPEN_AI_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    def __init__(self, model):
        self.model = model

    def get_response(self, messages, max_tokens=100):
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
        }
        response = requests.post(self.API_URL, headers=self.OPEN_AI_HEADERS, json=data)
        return response

    def model_setter(self, model):
        self.model = model

