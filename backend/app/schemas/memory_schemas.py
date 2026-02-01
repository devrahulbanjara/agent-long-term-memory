from pydantic import BaseModel


class ExtractedMemory(BaseModel):
    facts: list[str]
