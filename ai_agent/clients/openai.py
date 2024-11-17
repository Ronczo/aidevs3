import openai
from langfuse.decorators import langfuse_context, observe
from clients.langfuse import LangfuseClient
from schemas.context import Context

OPENAI_MODELS = {"4o-mini": "gpt-4o-mini", "4o": "gpt-4o", "4o-large": "gpt-4o-large"}


class OpenAIClient:
    def __init__(self, client=openai, model: str = OPENAI_MODELS["4o-mini"]):
        self.client = client
        self.model = model
        self.langfuse = LangfuseClient()

    @observe
    def chat(self, messages: [list[dict]], context: Context | None = None):
        if context:
            langfuse_context.update_current_trace(
                name="Tracing OpenAI Chat",
                session_id=context.session_id,
                user_id=context.user_id,
            )
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=1,
            max_tokens=400
        )

    def prepare_message_with_local_image(self, message: dict, image_url: str):
        message["content"].append(
            {
                "type": "image_url",
                "image_url": {"url": image_url},
            }
        )
        return message

    @staticmethod
    def prepare_message_with_image_url(image_url: str, text: str, role: str = "user"):
        return {
            "role": role,
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                },
                {
                    "type": "text",
                    "text": text,
                },
            ],
        }

    def generate_image_response(self, prompt: str, n: int = 1, size: str = "1024x1024"):
        response = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            n=n,
            size=size,
        )
        return response

    @staticmethod
    def get_url_of_generated_image(response):
        try:
            url = response.data[0].url
        except Exception:
            url = None
        return url

    @staticmethod
    def prepare_message(content: str, role: str = "user"):
        return {"role": role, "content": content}

    @staticmethod
    def get_content(response):
        try:
            content = response.choices[0].message.content
        except Exception as e:
            content = None
        return content

    def set_model(self, model: str):
        self.model = model
