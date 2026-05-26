import os
import json
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from src.loader import get_file_metadata
from src.chunker import split_documents
from src.vector_store import VectorStore
from src.retriever import Retriever
from src.analyzer import LLMAnalyzer
from src.card_builder import parse_llm_output, build_v2_card

app = FastAPI(title="Auto-Character-RAG API para Silly Tavern")

# Load configs
with open("config.json", "r") as f:
    config = json.load(f)

# Instanciar componentes globais
vector_store = VectorStore(
    db_dir=config["paths"]["vector_db_dir"],
    collection_name="novels_db",
    model_name=config["embeddings"]["model_name"],
)
retriever = Retriever(vector_store=vector_store)
analyzer = LLMAnalyzer(
    base_url=config["llm"]["base_url"],
    api_key=config["llm"]["api_key"],
    model_name=config["llm"]["model_name"],
    temperature=config["llm"]["temperature"],
)


class CardRequest(BaseModel):
    character_name: str


@app.post("/api/v1/ingest")
async def ingest_novels(background_tasks: BackgroundTasks):
    """
    Lê as novels na pasta data/novels e vetoriza em background.
    """

    def ingest_task():
        novels_dir = config["paths"]["novels_dir"]
        docs = get_file_metadata(novels_dir)
        if not docs:
            print("Nenhum arquivo encontrado para ingestão.")
            return

        chunks = split_documents(
            docs,
            chunk_size=config["embeddings"]["chunk_size"],
            chunk_overlap=config["embeddings"]["chunk_overlap"],
        )
        vector_store.ingest_chunks(chunks)

    background_tasks.add_task(ingest_task)
    return {"message": "Ingestão iniciada em background. Cheque os logs do servidor."}


@app.post("/api/v1/generate_card")
async def generate_card(request: CardRequest):
    """
    Faz o RAG, analisa e gera o card para o personagem solicitado.
    """
    char_name = request.character_name

    # 1. Recuperar contexto
    context = retriever.retrieve_for_character(char_name)
    if not context.strip():
        return {
            "error": "Nenhum contexto encontrado no banco de dados. Você já fez a ingestão das novels?"
        }

    # 2. Extrair informações consolidadas
    extracted_info = analyzer.extract_character_info(char_name, context)

    # 3. Gerar conteúdo do card
    llm_output = analyzer.generate_card_content(char_name, extracted_info)

    # 4. Construir e salvar o JSON
    parsed_data = parse_llm_output(llm_output)
    output_dir = config["paths"]["output_dir"]
    file_path = build_v2_card(char_name, parsed_data, output_dir)

    return {
        "message": "Card gerado com sucesso!",
        "file_path": file_path,
        "data": parsed_data,
    }


if __name__ == "__main__":
    import uvicorn

    print("Iniciando API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
