from dataclasses import dataclass

@dataclass
class LLMSettings:
    temperature: float
    model: str

def get_settings() -> LLMSettings:
    return LLMSettings(
        temperature = 0.0,
        model = "gpt-4.1-nano"
    )  
