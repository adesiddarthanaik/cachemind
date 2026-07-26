import time
import uuid

from fastapi import APIRouter, Response

from app.models.chat_completion_request import ChatCompletionRequest
from app.models.chat_completion_response import (
    ChatCompletionResponse,
    Choice,
    ResponseMessage,
    Usage,
)

from app.services.chat_service import ChatService

router = APIRouter()

chat_service = ChatService()


@router.post("/chat/completions")
def chat_completion(request: ChatCompletionRequest, response: Response):

    # ------------------------------------
    # Extract System Prompt + User Prompt
    # ------------------------------------

    system_prompt = ""

    user_prompt = ""

    for message in request.messages:

        if message.role == "system":
            system_prompt = message.content

        elif message.role == "user":
            user_prompt = message.content

    if not system_prompt:

        system_prompt = "You are a helpful AI assistant."

    # ------------------------------------
    # Chat Service
    # ------------------------------------

    result = chat_service.ask(
        prompt=user_prompt,
        model=request.model,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        system_prompt=system_prompt,
    )

    # ------------------------------------
    # Cache Headers
    # ------------------------------------

    if result["source"] == "semantic-cache":

        response.headers["X-Cache"] = "HIT"
        response.headers["X-Provider"] = "semantic-cache"
        response.headers["X-Similarity"] = str(result["similarity"])

    else:

        response.headers["X-Cache"] = "MISS"
        response.headers["X-Provider"] = request.model

    # ------------------------------------
    # OpenAI Compatible Response
    # ------------------------------------

    answer = result["response"]

    return ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4().hex}",
        object="chat.completion",
        created=int(time.time()),
        model=request.model,
        choices=[
            Choice(
                index=0,
                message=ResponseMessage(role="assistant", content=answer),
                finish_reason="stop",
            )
        ],
        usage=Usage(prompt_tokens=10, completion_tokens=15, total_tokens=25),
    )
