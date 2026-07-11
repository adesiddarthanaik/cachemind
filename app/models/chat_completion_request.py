from typing import List
from pydantic import BaseModel

from app.models.message import Message


class ChatCompletionRequest(BaseModel):

    model: str

    messages: List[Message]

    temperature: float = 0.7

    max_tokens: int = 512

    stream: bool = False