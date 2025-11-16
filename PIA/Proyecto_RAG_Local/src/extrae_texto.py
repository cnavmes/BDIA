import os
import json
import requests
import fitz  # PyMuPDF
import trafilatura
import re
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import (
    TEXTOS_LIMPIOS_DIR as OUTPUT_DIR,
    DOCS_ORIGINALES_DIR as OUTPUT_ORIGIN_PDFS,
    REQUEST_HEADERS,
    SOURCES_LIST
)



with open(SOURCES_LIST, "r", encoding="utf-8") as f:
    SOURCES = json.load(f)


def clean_text(text: str) -> str:
    """Limpia el texto de espacios en blanco anómalos."""
    if not text:
        return ""
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = '\n'.join([line.strip() for line in text.split('\n')])
    text = re.sub(r'\n\n+', '\n\n', text).strip()
    return text

def extract_text_from_pdf(url: str) -> str:
    """Extrae y limpia el texto de una URL PDF."""
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=15)
        response.raise_for_status()
        pdf_bytes = response.content
        full_text = ""
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            logging.info(f"Procesando PDF {url} ({doc.page_count} páginas)...")
            for page_num, page in enumerate(doc):
                page_text = page.get_text("text")
                lines = page_text.split('\n')
                cleaned_lines = [line for line in lines if len(line.strip()) >= 5 or not any(char.isdigit() for char in line)]
                page_text_cleaned = '\n'.join(cleaned_lines)
                full_text += page_text_cleaned + f"\n\n--- (Fin Página {page_num + 1}) ---\n\n"
        return clean_text(full_text)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al descargar PDF {url}: {e}")
        return ""
    except Exception as e:
        logging.error(f"Error procesando PDF {url}: {e}")
        return ""

def download_pdf_original(url: str, title: str):
    """Descarga y guarda el PDF original si la URL es .pdf."""
    try:
        if not os.path.exists(OUTPUT_ORIGIN_PDFS):
            os.makedirs(OUTPUT_ORIGIN_PDFS)
        response = requests.get(url, headers=REQUEST_HEADERS, stream=True, timeout=15)
        response.raise_for_status()
        safe_filename = re.sub(r'[^a-z0-9]+', '_', title.lower().strip()) + ".pdf"
        filepath = os.path.join(OUTPUT_ORIGIN_PDFS, safe_filename)
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
        logging.info(f"PDF original guardado en: {filepath}")
    except Exception as e:
        logging.error(f"Error al descargar PDF original {url}: {e}")

def process_html_and_nested_pdfs(url: str, title: str) -> str:
    """
    Extrae el texto principal de una página HTML y PDFs anidados.
    También descarga los PDFs anidados.
    """
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=15)
        response.raise_for_status()
        html_content = response.text
        logging.info(f"Extrayendo texto principal de HTML: {url}")
        main_page_text = trafilatura.extract(html_content, include_comments=False, include_tables=True, deduplicate=True) or ""
        soup = BeautifulSoup(html_content, 'html.parser')
        pdf_links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.lower().endswith('.pdf'):
                absolute_pdf_url = urljoin(url, href)
                pdf_links.append(absolute_pdf_url)
        nested_pdf_text = ""
        if pdf_links:
            unique_links = set(pdf_links)
            logging.info(f"Se encontraron {len(unique_links)} PDFs anidados únicos.")
            for pdf_url in unique_links:
                short_title = f"{title}_anidado"
                download_pdf_original(pdf_url, short_title)
                logging.info(f"Procesando PDF anidado: {pdf_url}")
                nested_pdf_text += f"\n\n--- INICIO PDF ANIDADO ({pdf_url}) ---\n\n"
                nested_pdf_text += extract_text_from_pdf(pdf_url)
                nested_pdf_text += f"\n\n--- FIN PDF ANIDADO ({pdf_url}) ---\n\n"
        else:
            logging.info("No se encontraron PDFs anidados.")
        combined_text = main_page_text + nested_pdf_text
        return clean_text(combined_text)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al descargar HTML {url}: {e}")
        return ""
    except Exception as e:
        logging.error(f"Error procesando HTML {url}: {e}")
        return ""

def save_text_to_file(title: str, content: str, url: str):
    """Guarda el contenido limpio en un archivo .txt."""
    if not content:
        logging.warning(f"No se guardó contenido para '{title}' (URL: {url}) porque estaba vacío.")
        return
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    safe_filename = re.sub(r'[^a-z0-9]+', '_', title.lower().strip()) + ".txt"
    filepath = os.path.join(OUTPUT_DIR, safe_filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"FUENTE_ORIGINAL: {url}\n")
            f.write(f"TITULO: {title}\n")
            f.write("----------------------------------------\n\n")
            f.write(content)
        logging.info(f"Texto limpio guardado en: {filepath}")
    except IOError as e:
        logging.error(f"Error al guardar archivo {filepath}: {e}")


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(OUTPUT_ORIGIN_PDFS):
        os.makedirs(OUTPUT_ORIGIN_PDFS)
    logging.info(f"Iniciando procesamiento de {len(SOURCES)} fuentes...")
    for source in SOURCES:
        title = source['title']
        url = source['url']
        logging.info(f"Procesando: '{title}' ({url})")
        cleaned_content = ""
        if url.lower().endswith('.pdf'):
            cleaned_content = extract_text_from_pdf(url)
            download_pdf_original(url, title)
        else:
            cleaned_content = process_html_and_nested_pdfs(url, title)
        save_text_to_file(title, cleaned_content, url)
    logging.info("--- Proceso completado ---")


if __name__ == "__main__":
    main()
