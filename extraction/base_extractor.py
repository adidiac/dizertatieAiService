# extraction/base_extractor.py

from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> dict:
        """Extract psychometric scores from text."""
        pass
