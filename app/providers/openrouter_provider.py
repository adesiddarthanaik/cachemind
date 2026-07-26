import requests

from app.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
)
from app.providers.base_provider import BaseProvider
from app.exceptions import ProviderException


class OpenRouterProvider(BaseProvider):
    """
    OpenRouter Provider
    """

    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = OPENROUTER_BASE_URL

        print("\n" + "=" * 60)
        print("OpenRouter Provider Initialized")

        if self.api_key:
            print(f"API Key Loaded : {self.api_key[:15]}...")
            print(f"API Key Length : {len(self.api_key)}")
        else:
            print("API Key Loaded : None")

        print(f"Base URL       : {self.base_url}")
        print("=" * 60 + "\n")

        if not self.api_key:
            raise ProviderException("OPENROUTER_API_KEY not found.")

    def generate(
        self,
        prompt: str,
        model: str,
        stream: bool = False,
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
            "stream": stream,
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )

            # Helpful debugging information
            print("\n===== OpenRouter Request =====")
            print("URL:", f"{self.base_url}/chat/completions")
            print("Model:", model)
            print("Status Code:", response.status_code)

            if response.status_code != 200:
                print("Response:", response.text)

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except requests.exceptions.HTTPError as e:
            raise ProviderException(
                f"OpenRouter HTTP Error ({response.status_code}): {response.text}"
            ) from e

        except requests.exceptions.RequestException as e:
            raise ProviderException(f"OpenRouter Request Error: {e}") from e

        except Exception as e:
            raise ProviderException(f"OpenRouter Error: {e}") from e
