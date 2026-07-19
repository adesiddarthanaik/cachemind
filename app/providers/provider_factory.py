from app.providers.openrouter_provider import OpenRouterProvider
from app.providers.ollama_provider import OllamaProvider

from app.exceptions import ProviderException


class ProviderFactory:
    """
    Factory responsible for selecting the appropriate LLM provider
    based on the model name.
    """

    PROVIDERS = {
        # ---------- Cloud Models ----------
        "gpt": OpenRouterProvider,
        "deepseek": OpenRouterProvider,
        "gemma": OpenRouterProvider,
        "claude": OpenRouterProvider,
        "gemini": OpenRouterProvider,

        # ---------- Local Models ----------
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

        model = model.strip().lower()

        for prefix, provider_cls in cls.PROVIDERS.items():

            if model.startswith(prefix):
                return provider_cls()

        supported = ", ".join(sorted(cls.PROVIDERS.keys()))

        raise ProviderException(
            f"Unsupported model '{model}'. "
            f"Supported prefixes: {supported}"
        )