from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict


def split_documents(
    docs_with_metadata: List[Dict], chunk_size: int = 1500, chunk_overlap: int = 300
) -> List[Dict]:
    """
    Recebe os documentos (com metadados) e divide em pedaços menores (chunks).
    Preserva as quebras de parágrafo e sentenças (melhor para novels).
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""],
        length_function=len,
    )

    chunks = []
    for doc in docs_with_metadata:
        content = doc["content"]
        source = doc["metadata"]["source"]

        split_texts = text_splitter.split_text(content)
        for i, text in enumerate(split_texts):
            chunks.append(
                {"content": text, "metadata": {"source": source, "chunk_id": i}}
            )

    return chunks
