from abc import ABC, abstractmethod

class MessengerBase(ABC):
    def __init__(self, message_received_callback):
        self.message_received_callback = message_received_callback

    @abstractmethod
    async def send_user_message(self, message):
        pass

    @abstractmethod
    async def send_user_image(self, message):
        pass
    
    @abstractmethod
    async def receive_user_message(self, message):
        pass

    @abstractmethod
    def run(self):
        pass