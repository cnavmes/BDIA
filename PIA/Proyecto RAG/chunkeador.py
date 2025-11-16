import os
import json

# Parámetros configurables
txt_folder = '/home/crixo/dev/BDIA/PIA/Proyecto RAG/textos_limpios'
output_json = '/Volumes/MacEx/DEV/BDIA/PIA/Proyecto_RAG_Local/todos_los_chunks.json'
chunk_size = 300        # palabras
overlap = 50            # palabras

chunk_list = []

for filename in os.listdir(txt_folder):
    if filename.endswith('.txt'):
        path = os.path.join(txt_folder, filename)
        with open(path, encoding='utf-8') as f:
            text = f.read()
            words = text.split()
            start = 0
            chunk_id = 1
            while start < len(words):
                end = start + chunk_size
                chunk_words = words[start:end]
                chunk_text = ' '.join(chunk_words)
                chunk_list.append({
                    "text": chunk_text,
                    "source": filename,
                    "chunk_id": chunk_id,
                })
                start += chunk_size - overlap
                chunk_id += 1

with open(output_json, 'w', encoding='utf-8') as fjson:
    json.dump(chunk_list, fjson, ensure_ascii=False, indent=2)
