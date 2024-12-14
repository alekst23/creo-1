from .vision_client import VisionClientBase
import requests

class VisionClient(VisionClientBase):
    def __init__(self):
        self.host = 'http://localhost:8000'
    
    def generate_image(self, prompt: str, width: int=512, height: int=512, config: dict={}) -> str:
        """
        Generate an image based on the prompt and returns a URL to the resource
        """
        # Make an HTTP POST request to localhost with the parameters
        response = requests.post(self.host+"/generate_image", json={'description': prompt, 'width': width, 'height': height})
        
        # Process the response and return the URL
        url = response.json()
        return url
    