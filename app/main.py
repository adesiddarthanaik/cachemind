from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.chat_service import ChatService
from app.services.health_service import HealthService
from app.services.metrics_service import MetricsService

from app.exceptions import (
    CacheException,
    EmbeddingException,
    ProviderException,
    VectorStoreException,
)

app = FastAPI(
    title="CacheMind",
    version="1.0.0"
)

# ---------------------------------
# Services
# ---------------------------------

chat_service = ChatService()
health_service = HealthService()
metrics_service = MetricsService()


# ---------------------------------
# Request Models
# ---------------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: list[Message]
    temperature: float = 0.7
    max_tokens: int = 512
    system_prompt: str = ""
    stream: bool = False


# ---------------------------------
# Routes
# ---------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to CacheMind"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/providers/health")
def providers_health():

    return health_service.check()


@app.get("/metrics")
def metrics():

    return metrics_service.stats()


@app.post("/v1/chat/completions")
def chat(request: ChatRequest):

    try:

        user_prompt = ""

        for message in request.messages:

            if message.role == "user":

                user_prompt = message.content

        result = chat_service.ask(
            prompt=user_prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            system_prompt=request.system_prompt,
            stream=request.stream,
        )

        if request.stream:

            return StreamingResponse(
                result,
                media_type="text/plain",
            )

        return result

    except (
        CacheException,
        EmbeddingException,
        ProviderException,
        VectorStoreException,
    ) as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )