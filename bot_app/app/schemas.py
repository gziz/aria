from typing import Dict, Optional

from pydantic import BaseModel, root_validator


class Message(BaseModel):
    text: Optional[str]

    @root_validator(pre=True)
    def check_text(cls, values):
        text = values.get("text")
        if text is None:
            raise ValueError("Either text or voice must be provided")
        return values


class AiChatMessage(BaseModel):
    role: str
    content: str

    def __str__(self):
        return f"{self.role}: {self.content}"


class Question(BaseModel):
    question: Optional[str]
    answer: Optional[str]
