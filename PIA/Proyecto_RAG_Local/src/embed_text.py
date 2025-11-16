import json
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from config import CHUNKS_JSON, CHUNKS_OUTPUT

def load_chunks(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    return chunks

def embed_texts(texts, model):
    return model.encode(texts, show_progress_bar=True)

def main():
    if not os.path.exists(CHUNKS_JSON):
        print(f"No se encontró el archivo de chunks: {CHUNKS_JSON}")
        return
    
    chunks = load_chunks(CHUNKS_JSON)
    texts = [chunk["text"] for chunk in chunks]
    ids = [f"{chunk['source']}_{chunk['chunk_id']}" for chunk in chunks]
    metadatas = [{"source": chunk["source"], "chunk_id": chunk["chunk_id"]} for chunk in chunks]

    print(f"Cargando modelo de embeddings...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print(f"Generando embeddings para {len(texts)} chunks...")
    embeddings = embed_texts(texts, model)

    
    client = chromadb.PersistentClient(
        path=CHUNKS_OUTPUT,
        settings=Settings()
    )

    collection = client.get_or_create_collection("normativa_andalucia")

    print("Insertando embeddings en la colección...")
    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids
    )

    

    print(f"Embeddings guardados persistentemente en {CHUNKS_OUTPUT}")

if __name__ == "__main__":
    main()
