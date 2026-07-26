import json
import os

import requests
from dotenv import load_dotenv

from app.providers.base_provider import BaseProvider
from app.exceptions import ProviderException

load_dotenv()


class OllamaProvider(BaseProvider):

    BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def generate(
        self,
        prompt: str,
        model: str,
        stream: bool = False,
    ):

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
        }

        try:

            response = requests.post(
                f"{self.BASE_URL}/api/generate",
                json=payload,
                stream=stream,
                timeout=120,
            )

            response.raise_for_status()

            if not stream:

                data = response.json()

                return data["response"]

            return self._stream_response(response)

        except requests.exceptions.RequestException as e:

            raise ProviderException(f"Ollama request failed: {e}")

        except Exception as e:

            raise ProviderException(f"Unexpected Ollama error: {e}")

    def _stream_response(self, response):

        try:

            for line in response.iter_lines():

                if not line:
                    continue

                chunk = json.loads(line.decode("utf-8"))

                if "response" in chunk:

                    yield chunk["response"]

                if chunk.get("done", False):

                    break

        except Exception as e:

            raise ProviderException(f"Streaming failed: {e}")
