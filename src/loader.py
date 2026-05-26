import os
import glob
from typing import List

def load_documents(directory_path: str) -> List[str]:
    """
    Lê todos os arquivos .txt do diretório especificado.
    Retorna uma lista contendo o texto completo de cada arquivo.
    """
    documents = []
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        print(f"Diretório {directory_path} criado. Adicione as novels lá.")
        return documents

    txt_files = glob.glob(os.path.join(directory_path, "*.txt"))
    for file_path in txt_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            documents.append(f.read())
            print(f"Carregado: {os.path.basename(file_path)}")
            
    return documents

def get_file_metadata(directory_path: str) -> List[dict]:
    """
    Lê arquivos .txt e mantém o texto com seus metadados (nome do arquivo).
    Útil para a ingestão com informações de origem.
    """
    docs_with_metadata = []
    if not os.path.exists(directory_path):
        return docs_with_metadata

    txt_files = glob.glob(os.path.join(directory_path, "*.txt"))
    for file_path in txt_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            docs_with_metadata.append({
                "content": f.read(),
                "metadata": {"source": os.path.basename(file_path)}
            })
            
    return docs_with_metadata
