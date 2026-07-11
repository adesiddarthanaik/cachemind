from typing import List
from pydantic import BaseModel


class ResponseMessage(BaseModel):

    role: str

    content: str


class Choice(BaseModel):

    index: int

    message: ResponseMessage

    finish_reason: str


class Usage(BaseModel):

    prompt_tokens: int

    completion_tokens: int

    total_tokens: int


class ChatCompletionResponse(BaseModel):

    id: str

    object: str

    created: int

    model: str

    choices: List[Choice]

    usage: Usage