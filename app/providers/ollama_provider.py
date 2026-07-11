from app.providers.base_provider import BaseProvider


class OllamaProvider(BaseProvider):
    """
    Placeholder implementation.

    Tomorrow we'll connect it to a real
    Ollama server.
    """

    def generate(
        self,
        prompt: str,
        model: str,
    ) -> str:

        return f"Ollama Response for: {prompt}"