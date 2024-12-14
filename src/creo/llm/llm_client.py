from abc import ABC, abstractmethod

class LLMClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_chat_completion(self, input_message: str, model_name: str=None) -> str:
        pass
        