import threading
import google.generativeai as genai
import vertexai
from vertexai.generative_models import GenerativeModel

from settings import load_api_key, load_project_id, load_region

class GenerativeChat:
    def __init__(self):
        # Configuração do Vertex AI
        self.api_key = load_api_key()
        self.project_id = load_project_id()
        self.region = load_region()

        # Configuração do Generative AI
        genai.configure(api_key=self.api_key)
        vertexai.init(project=self.project_id, location=self.region)
        self.model = GenerativeModel("gemini-1.5-flash-002")

    def gemini_response(self, message, callback):
        jsonResponse = self.model.generate_content(message)
        response = jsonResponse.candidates[0].content.parts[0].text
        callback(response)

    def get_response(self, message, callback):
        thread = threading.Thread(target=self.gemini_response, args=(message, callback))
        thread.start()