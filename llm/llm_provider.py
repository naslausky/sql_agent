from langchain_openai import ChatOpenAI
from config.llm_settings import get_settings

def get_llm():
    settings = get_settings()
    return ChatOpenAI(
        temperature = settings.temperature,
        model = settings.model,  # ou outro compatível
    )
