from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.models import ModelInfo
from config import MODEL_NAME, BASE_URL

def get_model_client():
    # Returns a configured Ollama client pointed at the local inference server
    return OllamaChatCompletionClient(
        model = MODEL_NAME,
        host = BASE_URL,
        streaming = True    
    )
