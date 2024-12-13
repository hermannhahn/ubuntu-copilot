import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
import google.generativeai as genai
from google.cloud import aiplatform


def multiturn_generate_content():
    vertexai.init(project="hcloud-321513", location="southamerica-east1")
    model = GenerativeModel(
        "gemini-1.0-pro-002",
    )
    chat = model.start_chat()


generation_config = {
    "max_output_tokens": 2048,
    "temperature": 1,
    "top_p": 1,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]

multiturn_generate_content()

parts = [
    Part(
        content="Olá, como você está?",
        part_type=Part.PartType.TEXT,
    ),
    Part(
        content="Estou bem, obrigado por perguntar. Como posso te ajudar?",
        part_type=Part.PartType.TEXT,
    ),
]
response = chat.generate_content(
    parts=parts,
    generation_config=generation_config,
    safety_settings=safety_settings,
)
print(response.text)
