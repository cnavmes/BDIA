import os
import re
import logging
from collections import OrderedDict

# --- 1. Configuración ---
# Directorio objetivo (se modificarán los archivos)
TARGET_DIR = "/home/crixo/dev/BDIA/PIA/Proyecto RAG/textos_limpios"

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 2. Función de Limpieza Profunda ---

def deep_clean_text_body(text: str) -> str:
    """
    Aplica una limpieza profunda al cuerpo del texto,
    corrigiendo los errores de versiones anteriores.
    """
    
    # ---------------------------------------------------------------------
    # 1. Eliminar marcadores de procesamiento de PDF/Página
    # Esto elimina el "ruido" que el script anterior introdujo.
    # ---------------------------------------------------------------------
    try:
        text = re.sub(r'---\s*\(Fin Página \d+\)\s*---', '', text)
        text = re.sub(r'---\s*INICIO PDF ANIDADO \(.*?\)\s*---', '', text)
        text = re.sub(r'---\s*FIN PDF ANIDADO \(.*?\)\s*---', '', text)
    except Exception as e:
        logging.warning(f"Error al eliminar marcadores: {e}")

    # ---------------------------------------------------------------------
    # 2. Eliminar caracteres de control (no imprimibles)
    # Este regex es una "lista negra": borra solo caracteres de 
    # control conocidos (como 'bell', 'backspace') pero CONSERVA
    # \n (salto de línea), \t (tab) y TODOS los caracteres imprimibles
    # (letras, NÚMEROS, símbolos, emojis, etc.).
    # ---------------------------------------------------------------------
    try:
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    except Exception as e:
        logging.warning(f"Error en limpieza de caracteres (Regex corregido): {e}")

    # ---------------------------------------------------------------------
    # 3. Eliminar párrafos duplicados (conservando el orden)
    # Esto responde a "eliminar repeticiones"
    # (Se divide por \n\n, se buscan únicos y se vuelve a unir)
    # ---------------------------------------------------------------------
    try:
        paragraphs = text.split('\n\n')
        # Usamos dict.fromkeys en Python 3.7+ (es un set ordenado)
        unique_paragraphs = list(dict.fromkeys(
            p.strip() for p in paragraphs if p.strip()
        ))
        text = '\n\n'.join(unique_paragraphs)
    except Exception as e:
        logging.warning(f"Error al eliminar párrafos duplicados: {e}")

    # ---------------------------------------------------------------------
    # 4. Eliminar palabras duplicadas consecutivas (ej. "el el" -> "el")
    # ---------------------------------------------------------------------
    try:
        text = re.sub(
            r'\b(\w+)\s+\1\b', 
            r'\1', 
            text, 
            flags=re.IGNORECASE
        )
    except Exception as e:
        logging.warning(f"Error en limpieza de palabras duplicadas: {e}")

    # ---------------------------------------------------------------------
    # 5. Normalización final de espacios en blanco
    # ---------------------------------------------------------------------
    text = re.sub(r'[ \t]+', ' ', text)       # Múltiples espacios/tabs -> 1 espacio
    text = re.sub(r'\n\s*\n', '\n\n', text)   # Líneas vacías -> max 1 (\n\n)
    text = '\n'.join([line.strip() for line in text.split('\n')]) # Espacios al inicio/fin de línea
    text = re.sub(r'\n\n+', '\n\n', text).strip() # Normalización final
    
    return text

# --- 3. Función Principal ---

def main():
    """
    Recorre la carpeta, limpia cada archivo y lo SOBRESCRIBE.
    """
    
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
                # 1. Leer el contenido original
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 2. Separar la cabecera de metadatos del cuerpo del texto
                header = ""
                body = ""
                
                if separator in content:
                    parts = content.split(separator, 1)
                    header = parts[0] + separator # Incluye el separador
                    body = parts[1]
                else:
                    logging.warning(f"No se encontró separador de cabecera en {filename}")
                    body = content

                # 3. Aplicar la limpieza profunda (CORREGIDA) SOLO al cuerpo
                cleaned_body = deep_clean_text_body(body)

                # 4. Volver a escribir el archivo (SOBRESCRIBIR)
                with open(filepath, 'w', encoding='utf-8') as f:
                    if header:
                        f.write(header)
                        f.write("\n\n") # Espacio entre cabecera y cuerpo
                    f.write(cleaned_body)
                    
            except Exception as e:
                logging.error(f"Error al procesar el archivo {filename}: {e}")

    logging.info(f"--- Proceso de limpieza profunda (corregido) completado ---")
    logging.info(f"Se han modificado {file_count} archivos en '{TARGET_DIR}'.")

# --- 4. Punto de Entrada ---
if __name__ == "__main__":
    main()