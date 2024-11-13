import openai
from langfuse.decorators import langfuse_context, observe
from clients.langfuse import LangfuseClient
from schemas.context import Context

OPENAI_MODELS = {"4o-mini": "gpt-4o-mini"}


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
        )

    def prepare_message(self, content: str, role: str = "user"):
        return {
            "role": role,
            "content": content
        }

    @staticmethod
    def get_content(response):
        try:
            content = response.choices[0].message.content
        except Exception as e:
            content = None
        return content

    def set_model(self, model: str):
        self.model = model