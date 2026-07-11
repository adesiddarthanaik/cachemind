import os

from app.providers.base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    """
    OpenAI Provider.
    Currently mocked.
    Later we'll replace the generate()
    implementation with the official SDK.
    """

    def generate(
        self,
        prompt: str,
        model: str,
    ) -> str:

        return f"OpenAI Response for: {prompt}"