from langfuse import Langfuse


from langfuse.decorators import langfuse_context

from settings import LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST


class LangfuseClient:
    def __init__(self):
        langfuse = Langfuse(
            public_key=LANGFUSE_PUBLIC_KEY,
            secret_key=LANGFUSE_SECRET_KEY,
            host=LANGFUSE_HOST,
        )
        self.client = langfuse
