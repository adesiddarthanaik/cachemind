import os
import requests

from dotenv import load_dotenv

from app.providers.base_provider import BaseProvider
from app.exceptions import ProviderException

load_dotenv()


class OpenRouterProvider(BaseProvider):
    """
    OpenRouter Provider
    """

    def __init__(self):

        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL")

        if not self.api_key:

            raise ProviderException(
                "OPENROUTER_API_KEY not found."
            )

    def generate(
        self,
        prompt: str,
        model: str,
    ) -> str:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        try:

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except Exception as e:

            raise ProviderException(
                f"OpenRouter Error: {e}"
            )