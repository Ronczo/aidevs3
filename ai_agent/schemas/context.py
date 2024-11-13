from pydantic import BaseModel

class Context(BaseModel):
    user_id: str
    session_id: str | None
