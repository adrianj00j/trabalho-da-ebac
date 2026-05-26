import json
import os
import re
from typing import Dict

def parse_llm_output(llm_output: str) -> Dict[str, str]:
    """
    Tenta fazer parse das seções geradas pelo LLM.
    """
    parsed = {
        "description": "",
        "personality": "",
        "mes_example": "",
        "first_mes": "",
        "scenario": ""
    }
    
    # regex basico para buscar as sessoes (ex: 1. [DESCRIPTION]: texto)
    patterns = {
        "description": r"\[DESCRIPTION\]:(.*?)(?:\[PERSONALITY\]|\[MES_EXAMPLE\]|\[FIRST_MES\]|\[SCENARIO\]|$)",
        "personality": r"\[PERSONALITY\]:(.*?)(?:\[DESCRIPTION\]|\[MES_EXAMPLE\]|\[FIRST_MES\]|\[SCENARIO\]|$)",
        "mes_example": r"\[MES_EXAMPLE\]:(.*?)(?:\[DESCRIPTION\]|\[PERSONALITY\]|\[FIRST_MES\]|\[SCENARIO\]|$)",
        "first_mes": r"\[FIRST_MES\]:(.*?)(?:\[DESCRIPTION\]|\[PERSONALITY\]|\[MES_EXAMPLE\]|\[SCENARIO\]|$)",
        "scenario": r"\[SCENARIO\]:(.*?)(?:\[DESCRIPTION\]|\[PERSONALITY\]|\[MES_EXAMPLE\]|\[FIRST_MES\]|$)"
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, llm_output, re.DOTALL)
        if match:
            parsed[key] = match.group(1).strip()
            
    return parsed

def build_v2_card(character_name: str, parsed_data: Dict[str, str], output_dir: str) -> str:
    """
    Constrói o JSON V2 padrão do Silly Tavern e salva no disco.
    """
    card = {
        "spec": "chara_card_v2",
        "spec_version": "2.0",
        "data": {
            "name": character_name,
            "description": parsed_data.get("description", ""),
            "personality": parsed_data.get("personality", ""),
            "scenario": parsed_data.get("scenario", ""),
            "first_mes": parsed_data.get("first_mes", ""),
            "mes_example": parsed_data.get("mes_example", ""),
            "creator_notes": "Gerado por Auto-Character-RAG",
            "system_prompt": "",
            "post_history_instructions": "",
            "tags": ["AI Generated", "Novel RAG"],
            "creator": "",
            "character_version": "1.0",
            "alternate_greetings": [],
            "extensions": {}
        }
    }
    
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{character_name.replace(' ', '_')}_card.json")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(card, f, ensure_ascii=False, indent=4)
        
    return file_path
