from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(ChatRequest):
    pass
