import uuid

from fastapi import APIRouter, Depends

from api.deps import get_openai_client
from clients.openai import OpenAIClient
from schemas.context import Context
from schemas.prompt import Prompt

router = APIRouter()


@router.get("/")
def hello_world():
    return {"message": "Hello, World!"}


@router.post("/chat/")
def chat(prompt: Prompt, open_ai: OpenAIClient = Depends(get_openai_client)):
    message = open_ai.prepare_message(prompt.prompt)
    messages = [message]
    session_id = prompt.session_id or str(uuid.uuid4())
    context = Context(user_id=prompt.user_id, session_id=session_id)
    response = open_ai.chat(messages, context=context)
    content = open_ai.get_content(response)
    return content
