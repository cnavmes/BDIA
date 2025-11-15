import os
import requests
import fitz  # PyMuPDF
import trafilatura
import re
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# --- 1. Definición de Fuentes ---
SOURCES = [
    {'title': 'Ley 1-2023 Atencion Temprana', 'url': 'https://www.juntadeandalucia.es/boja/2023/36/1'},
    {'title': 'Ley 4-2017 Derechos Discapacidad', 'url': 'https://www.rpdiscapacidad.gob.es/docs/Res_TEA.pdf'},
    {'title': 'Decreto 147-2002 Atencion Educativa NEAE', 'url': 'https://www.juntadeandalucia.es/organismos/desarrolloeducativoyformacionprofesional/areas/centros-educativos/atencion-diversidad.html'},
    {'title': 'Solicitud Grado Discapacidad', 'url': 'https://www.juntadeandalucia.es/servicios/sede/tramites/procedimientos/detalle/69.html'},
    {'title': 'Derechos y Prestaciones Discapacidad', 'url': 'https://www.juntadeandalucia.es/organismos/saludyconsumo/areas/salud-vida/adulta/paginas/ive-discapacidad.html'},
    {'title': 'Centros de Valoracion CVO', 'url': 'https://www.juntadeandalucia.es/organismos/inclusionsocialjuventudfamiliaseigualdad/areas/discapacidad/cvo.html'},
    {'title': 'Guia Prestaciones TEA Mirame PDF', 'url': 'https://www.mirame.org/main/wp-content/uploads/2022/01/prestaciones-servicios-TEA.pdf'},
    {'title': 'Guia Como Solicitar Discapacidad', 'url': 'https://andaluciainforma.eldiario.es/tramites/como-solicitar-de-forma-correcta-el-reconocimiento-del-grado-de-discapacidad-en-andalucia/'},
    {'title': 'Solicitud Dependencia', 'url': 'https://www.juntadeandalucia.es/organismos/inclusionsocialjuventudfamiliaseigualdad/areas/dependencia/solicitud.html'},
    {'title': 'Ventanilla Electronica Dependencia VED', 'url': 'https://www.juntadeandalucia.es/servicios/sede/ventanillas/dependencia.html'},
    {'title': 'Guia Ley Dependencia UNIR', 'url': 'https://www.unir.net/educacion/revista/noticias/como-solicitar-ley-dependencia-andalucia/'},
    {'title': 'Texto Ley 1-2023 Atencion Temprana BOJA', 'url': 'https://www.juntadeandalucia.es/boja/2023/36/1'},
    {'title': 'Portal Familias Necesidades Especiales', 'url': 'https://www.familiasandalucia.es/familias-con-necesidades-especiales/'},
    {'title': 'Listado Centros CAIT', 'url': 'https://www.juntadeandalucia.es/organismos/saludyconsumo/areas/salud-vida/adulta/paginas/ive-discapacidad.html'},
    {'title': 'Instruccion 2015 Deteccion Educativa', 'url': 'https://www.juntadeandalucia.es/organismos/desarrolloeducativoyformacionprofesional/areas/centros-educativos/atencion-diversidad.html'},
    {'title': 'Portal Escuela Familias TEA', 'url': 'https://www.juntadeandalucia.es/educacion/portals/web/escuela-familias/necesidades-especificas-de-apoyo-educativo/necesidades-educativas-especiales/trastornos-del-espectro-autista'},
    {'title': 'Portal Familias Consejeria Educacion', 'url': 'https://www.juntadeandalucia.es/educacion/portals/web/familias'},
    {'title': 'Convenio Educacion Autismo Andalucia 2020', 'url': 'https://www.defensordelpuebloandaluz.es/reclamamos-que-se-potencie-y-extienda-la-disponibilidad-de-aulas-especificas-de-atencion-al-alumnado'},
    {'title': 'Comunicado Apoyo Alumnado TEA Autismo Andalucia', 'url': 'https://www.autismoandalucia.org/entradas-autismo/comunicado-sobre-el-convenio-de-apoyo-al-alumnado-con-tea/'},
    {'title': 'Becas NEAE Ministerio', 'url': 'https://www.educacionfpydeportes.gob.es/servicios-al-ciudadano/catalogo/general/05/050140/ficha/050140-2024.html'},
    {'title': 'Ayudas Prestaciones Discapacidad JA', 'url': 'https://www.juntadeandalucia.es/temas/familias-igualdad/discapacidad/prestaciones.html'},
    {'title': 'Becas NEAE Andalucia Educaorienta', 'url': 'https://educaorientamalaga.com/ayudas-y-becas-para-alumnado-con-necesidades-educativas-en-andalucia/'},
    {'title': 'Ayudas Contratacion Cuidadores', 'url': 'https://criando247.com/ayudas-autonomia-discapacidad/'},
    {'title': 'Prestaciones Estatales Discapacidad SS', 'url': 'https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/PrestacionesPensionesTrabajadores/61fce0cb-bb6d-4bfa-8e83-61ec6e2bce86'},
    {'title': 'Autismo Andalucia Servicios', 'url': 'https://www.autismoandalucia.org/autismo/servicios-y-recursos/'},
    {'title': 'Autismo Sevilla Apoyos', 'url': 'https://www.autismosevilla.org/apoyos-individualizados.php'},
    {'title': 'Autismo Sevilla Apoyo Familiares', 'url': 'https://www.autismosevilla.org/blog/programas-de-apoyo-para-familiares-cuidadores-de-personas-con-tea/'}
]

# --- 2. Configuración de rutas ---
OUTPUT_DIR = "/home/crixo/dev/BDIA/PIA/Proyecto RAG/textos_limpios"
OUTPUT_ORIGIN_PDFS = "/home/crixo/dev/BDIA/PIA/Proyecto RAG/docs_originales"
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 3. Funciones ---
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

# --- 4. Función principal ---
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

# --- 5. Punto de entrada ---
if __name__ == "__main__":
    main()
