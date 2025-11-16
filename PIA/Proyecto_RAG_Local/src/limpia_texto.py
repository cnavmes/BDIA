import os
import re
import logging
from collections import OrderedDict

from config import TEXTOS_LIMPIOS_DIR as TARGET_DIR


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def deep_clean_text_body(text: str) -> str:
    """
    Aplica una limpieza profunda al cuerpo del texto,
    corrigiendo los errores de versiones anteriores.
    """
    try:
        text = re.sub(r'---\s*\(Fin Página \d+\)\s*---', '', text)
        text = re.sub(r'---\s*INICIO PDF ANIDADO \(.*?\)\s*---', '', text)
        text = re.sub(r'---\s*FIN PDF ANIDADO \(.*?\)\s*---', '', text)
    except Exception as e:
        logging.warning(f"Error al eliminar marcadores: {e}")

    try:
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    except Exception as e:
        logging.warning(f"Error en limpieza de caracteres (Regex corregido): {e}")

    try:
        paragraphs = text.split('\n\n')
        unique_paragraphs = list(dict.fromkeys(
            p.strip() for p in paragraphs if p.strip()
        ))
        text = '\n\n'.join(unique_paragraphs)
    except Exception as e:
        logging.warning(f"Error al eliminar párrafos duplicados: {e}")

    try:
        text = re.sub(
            r'\b(\w+)\s+\1\b', 
            r'\1', 
            text, 
            flags=re.IGNORECASE
        )
    except Exception as e:
        logging.warning(f"Error en limpieza de palabras duplicadas: {e}")

    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = '\n'.join([line.strip() for line in text.split('\n')])
    text = re.sub(r'\n\n+', '\n\n', text).strip()
    
    return text

def main():
    if not os.path.exists(TARGET_DIR):
        logging.error(f"El directorio objetivo no existe: {TARGET_DIR}")
        logging.error("Asegúrate de ejecutar primero el script de la Fase 3.2b (extracción)")
        return

    logging.info(f"Iniciando limpieza profunda (MODO SOBRESCRIBIR) en: '{TARGET_DIR}'...")
    logging.warning("¡Esta acción MODIFICARÁ los archivos originales!")

    file_count = 0
    separator = "----------------------------------------"

    for filename in os.listdir(TARGET_DIR):
        if filename.endswith(".txt"):
            file_count += 1
            filepath = os.path.join(TARGET_DIR, filename)

            logging.info(f"Procesando y modificando: {filename}")

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                header = ""
                body = ""

                if separator in content:
                    parts = content.split(separator, 1)
                    header = parts[0] + separator
                    body = parts[1]
                else:
                    logging.warning(f"No se encontró separador de cabecera en {filename}")
                    body = content

                cleaned_body = deep_clean_text_body(body)

                with open(filepath, 'w', encoding='utf-8') as f:
                    if header:
                        f.write(header)
                        f.write("\n\n")
                    f.write(cleaned_body)

            except Exception as e:
                logging.error(f"Error al procesar el archivo {filename}: {e}")

    logging.info(f"--- Proceso de limpieza profunda (corregido) completado ---")
    logging.info(f"Se han modificado {file_count} archivos en '{TARGET_DIR}'.")

if __name__ == "__main__":
    main()
