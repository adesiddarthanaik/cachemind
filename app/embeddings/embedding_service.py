from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    """
    Abstract base class for all embedding providers.
    """

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        pass
