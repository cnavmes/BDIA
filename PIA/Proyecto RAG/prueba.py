import os
import json
import time
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


total_per_batch = 10
with open("todos_los_chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)
    total_chunks = len(chunks)


embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Conecta a la base Chroma 
vector_store = Chroma(
    collection_name="rag_collection",
    embedding_function=embeddings,
    persist_directory="/home/crixo/dev/BDIA/PIA/Proyecto RAG/chroma_db"
)

current = 2153
while current < total_chunks:
    end = min(current + total_per_batch, total_chunks)
    batch = chunks[current:end]
    texts = [c["text"] for c in batch]
    metas = [{"source": c["source"], "chunk_id": c["chunk_id"]} for c in batch]
    print(f"Añadiendo chunks {current+1} a {end}...")
    try:
        vector_store.add_texts(texts=texts, metadatas=metas)
        print(f"   → OK: {end-current} procesados.")
    except Exception as e:
        print(f"   ¡ERROR!: {e}\nEspera unos minutos y ejecuta de nuevo (el proceso sigue donde se queda).")
        break  
    current += total_per_batch
    
    time.sleep(10)

print(f"Proceso completado hasta chunk {current} de {total_chunks}.")
