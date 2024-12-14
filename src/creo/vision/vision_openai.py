from openai import OpenAI
from .vision_client import VisionClientBase

class VisionClient(VisionClientBase):
    def __init__(self):
        self.client = OpenAI()
        self.model="dall-e-3"

    def generate_image(self, prompt, width=1024, height=1024, config={}):
        res = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size=f"{width}x{height}",
            quality=config.get("quality","standard"),
            n=1
        )

        return res.data[0].url