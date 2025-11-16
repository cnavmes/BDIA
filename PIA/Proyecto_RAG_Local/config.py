import os

BASE_DIR = os.path.expanduser('/Volumes/MacEx/DEV/BDIA/PIA/Proyecto_RAG_Local')

DOCS_DIR = os.path.join(BASE_DIR, "docs")
DOCS_ORIGINALES_DIR = os.path.join(DOCS_DIR, "docs_originales")

TEXTOS_LIMPIOS_DIR = os.path.join(BASE_DIR, "data", "textos_limpios")
CHUNKS_OUTPUT = os.path.join(BASE_DIR, "data", "chunks")

SOURCES_LIST = os.path.join(DOCS_DIR, 'fuentes', 'fuentes.json')

CHUNKS_JSON = os.path.join(CHUNKS_OUTPUT, "todos_los_chunks.json")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
SEPARADOR = "----------------------------------------"

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
}
