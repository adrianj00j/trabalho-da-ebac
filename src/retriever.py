from typing import List, Dict
from src.vector_store import VectorStore

class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve_for_character(self, character_name: str, n_results: int = 15) -> str:
        """
        Faz várias perguntas chave para resgatar os chunks mais relevantes sobre o personagem.
        """
        queries = [
            f"Como é a aparência de {character_name}? Quais roupas veste?",
            f"Como {character_name} age? Qual sua personalidade?",
            f"Qual é o passado de {character_name}? História e mundo.",
            f"Como {character_name} fala? Exemplos de diálogo."
        ]
        
        all_chunks = []
        seen_contents = set()
        
        for q in queries:
            results = self.vector_store.query(q, n_results=n_results)
            for r in results:
                if r["content"] not in seen_contents:
                    seen_contents.add(r["content"])
                    all_chunks.append(r)
                    
        # Ordenar os chunks pode ajudar (ex: pelo chunk_id) ou apenas juntar
        context_text = "\n\n---\n\n".join([c["content"] for c in all_chunks])
        return context_text
