import time

from app.providers.base_provider import BaseProvider


class FakeProvider(BaseProvider):

    def generate(self, prompt: str, model: str) -> str:

        time.sleep(2)

        return f"AI Response for: {prompt}"
