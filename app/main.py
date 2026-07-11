from fastapi import FastAPI

from app.api.chat_routes import router as chat_router
from app.exception_handlers import register_exception_handlers

app = FastAPI(
    title="CacheMind",
    version="0.5.0",
    description="Drop-in Semantic Cache for LLM APIs"
)

# Register Global Exception Handlers
register_exception_handlers(app)


@app.get("/")
def root():

    return {
        "message": "CacheMind Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


app.include_router(
    chat_router,
    prefix="/v1",
    tags=["OpenAI Compatible API"]
)