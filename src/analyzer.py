import requests
import json
from src.prompts import CHARACTER_EXTRACTION_PROMPT, CARD_GENERATION_PROMPT

class LLMAnalyzer:
    def __init__(self, base_url: str, api_key: str, model_name: str, temperature: float = 0.7):
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        
    def _call_llm(self, prompt: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature
        }
        
        # Endpoint padrão OpenAI (chat/completions)
        endpoint = f"{self.base_url.rstrip('/')}/chat/completions"
        
        print(f"Chamando LLM em {endpoint}...")
        response = requests.post(endpoint, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Erro na API do LLM: {response.status_code} - {response.text}")

    def extract_character_info(self, character_name: str, context: str) -> str:
        prompt = CHARACTER_EXTRACTION_PROMPT.format(character_name=character_name, context=context)
        return self._call_llm(prompt)
        
    def generate_card_content(self, character_name: str, extracted_info: str) -> str:
        prompt = CARD_GENERATION_PROMPT.format(character_name=character_name, extracted_info=extracted_info)
        return self._call_llm(prompt)
