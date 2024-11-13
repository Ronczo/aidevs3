from pydantic import BaseModel


class Prompt(BaseModel):
    prompt: str
    user_id: str
    session_id: str | None

