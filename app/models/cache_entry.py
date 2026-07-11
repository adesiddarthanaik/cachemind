from pydantic import BaseModel
from datetime import datetime


class CacheEntry(BaseModel):
    """
    Represents one cached LLM response.
    """

    id: int

    prompt: str

    response: str

    model: str

    system_prompt_hash: str

    temperature: float

    max_tokens: int

    timestamp: datetime

    hit_count: int = 0

    ttl: int = 3600