from app.providers.openrouter_provider import OpenRouterProvider
from app.providers.ollama_provider import OllamaProvider

from app.exceptions import ProviderException


class ProviderFactory:
    """
    Factory responsible for selecting the correct provider.
    """

    PROVIDERS = {

        # Cloud Models (OpenRouter)
        "gpt": OpenRouterProvider,
        "deepseek": OpenRouterProvider,
        "gemma": OpenRouterProvider,
        "claude": OpenRouterProvider,
        "gemini": OpenRouterProvider,

        # Local Models (Ollama)
        "llama": OllamaProvider,
        "mistral": OllamaProvider,
        "phi": OllamaProvider,
        "qwen": OllamaProvider,

    }

    @classmethod
    def get_provider(cls, model: str):

        if not model:

            raise ProviderException(
                "Model name cannot be empty."
            )

        model = model.lower()

        for prefix, provider in cls.PROVIDERS.items():

            if model.startswith(prefix):

                return provider()

        raise ProviderException(
            f"Unsupported model: '{model}'. "
            f"Supported model prefixes are: {', '.join(cls.PROVIDERS.keys())}"
        )