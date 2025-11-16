import os
import json
from config import (
    TEXTOS_LIMPIOS_DIR as TXT_FOLDER,
    CHUNKS_JSON as OUTPUT_JSON,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

def create_chunks(text, chunk_size, overlap):
    words = text.split()
    start = 0
    chunk_id = 1
    chunks = []
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = ' '.join(chunk_words)
        chunks.append({
            "text": chunk_text,
            "chunk_id": chunk_id
        })
        start += chunk_size - overlap
        chunk_id += 1
    return chunks

def main():
    chunk_list = []

    if not os.path.exists(TXT_FOLDER):
        print(f"Error: La carpeta {TXT_FOLDER} no existe. Asegúrate que el path es correcto.")
        return

    for filename in os.listdir(TXT_FOLDER):
        if filename.endswith('.txt'):
            path = os.path.join(TXT_FOLDER, filename)
            with open(path, encoding='utf-8') as f:
                text = f.read()
                chunks = create_chunks(text, CHUNK_SIZE, CHUNK_OVERLAP)
                for chunk in chunks:
                    chunk_list.append({
                        "text": chunk["text"],
                        "source": filename,
                        "chunk_id": chunk["chunk_id"]
                    })

    
    output_dir = os.path.dirname(OUTPUT_JSON)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as fjson:
        json.dump(chunk_list, fjson, ensure_ascii=False, indent=2)
    print(f"Chunks guardados en {OUTPUT_JSON}, total chunks: {len(chunk_list)}")

if __name__ == "__main__":
    main()
