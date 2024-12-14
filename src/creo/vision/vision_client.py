from abc import ABC, abstractmethod

from openai import OpenAI

class VisionClientBase(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def generate_image(self, prompt: str, width: int, height: int, config: dict) -> str:
        """
        Generate an image based on the prompt and returns a URL to the resource
        """
        pass