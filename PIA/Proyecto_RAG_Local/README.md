# Proyecto RAG Local con LM Studio

Este proyecto implementa un sistema de Retrieval-Augmented Generation (RAG) que utiliza una base de datos vectorial local y se conecta a un Large Language Model (LLM) a través de LM Studio. El sistema está diseñado para responder preguntas sobre un conjunto de documentos específicos, en este caso, normativa y documentación relacionada con el Trastorno del Espectro Autista (TEA) en Andalucía.

## Descripción General

El proyecto consta de dos componentes principales:

1.  **Pipeline de Procesamiento de Datos**: Un conjunto de scripts que extraen texto de diversas fuentes (PDF y HTML), lo limpian, lo dividen en fragmentos (chunks) y generan embeddings para almacenarlos en una base de datos vectorial ChromaDB.
2.  **Aplicación Web de Chat**: Una aplicación Flask que proporciona una interfaz de chat para que los usuarios puedan hacer preguntas. La aplicación busca en la base de datos vectorial los fragmentos de texto más relevantes para la pregunta del usuario, los utiliza como contexto y llama a un LLM local para generar una respuesta.

## Características

-   **Extracción de Texto Multi-fuente**: Extrae texto de archivos PDF y páginas web HTML, incluyendo PDFs anidados.
-   **Limpieza de Texto**: Realiza una limpieza profunda del texto extraído para eliminar ruido y mejorar la calidad de los datos.
-   **Chunking y Embedding**: Divide el texto en fragmentos superpuestos y genera embeddings utilizando `sentence-transformers`.
-   **Base de Datos Vectorial Local**: Utiliza ChromaDB para almacenar los embeddings de forma persistente.
-   **Integración con LLM Local**: Se conecta a un LLM que se ejecuta localmente a través de LM Studio.
-   **Interfaz de Chat Web**: Proporciona una interfaz de usuario sencilla para interactuar con el sistema.

## Estructura del Proyecto

```
/
├── app.py                  # Aplicación principal de Flask y orquestador del pipeline
├── config.py               # Archivo de configuración con rutas y parámetros
├── requirements.txt        # Dependencias de Python
├── data/
│   ├── chunks/             # Base de datos ChromaDB y chunks en formato JSON
│   └── textos_limpios/     # Archivos de texto limpios extraídos de las fuentes
├── docs/
│   ├── docs_originales/    # Archivos PDF originales descargados
│   └── fuentes/
│       └── fuentes.json    # Lista de fuentes de datos (URLs)
└── src/
    ├── extrae_texto.py     # Script para extraer texto de las fuentes
    ├── limpia_texto.py     # Script para limpiar el texto extraído
    ├── chunk.py            # Script para dividir el texto en chunks
    └── embed_text.py       # Script para generar y almacenar los embeddings
```

## Instalación

1.  **Clonar el repositorio**:
    ```bash
    git clone <url-del-repositorio>
    cd <nombre-del-repositorio>
    ```

2.  **Crear un entorno virtual e instalar dependencias**:
    Se recomienda utilizar un entorno virtual para gestionar las dependencias.

    ```bash
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configurar LM Studio**:
    - Descargue e instale [LM Studio](https://lmstudio.ai/).
    - Inicie LM Studio y descargue un modelo de lenguaje (por ejemplo, `gemma-3-12b`).
    - Inicie el servidor local en LM Studio. La aplicación se conectará a `http://localhost:1234/v1/chat/completions`.

## Uso

1.  **Ejecutar la aplicación**:
    ```bash
    python app.py
    ```
    Al ejecutar este comando, se iniciará el pipeline de procesamiento de datos. Esto puede tardar un tiempo la primera vez, ya que descargará los documentos, los procesará y generará los embeddings. Una vez que el pipeline haya finalizado, la aplicación web Flask se iniciará automáticamente.

2.  **Acceder a la interfaz de chat**:
    Abra su navegador web y vaya a la dirección que se muestra en la consola (generalmente `http://127.0.0.1:5000`).

3.  **Chatear con el sistema**:
    Escriba sus preguntas en el cuadro de texto y presione "Enviar". El sistema buscará en los documentos de la base de datos y utilizará la información encontrada para generar una respuesta con el LLM.

## Cómo Funciona el Pipeline

El pipeline de datos se ejecuta automáticamente al iniciar `app.py` a través de la función `main_pipeline()`.

1.  **`extract_main()` (`src/extrae_texto.py`)**: Lee las URLs del archivo `docs/fuentes/fuentes.json` y extrae el texto de cada fuente. Guarda los textos limpios en `data/textos_limpios/`.
2.  **`clean_main()` (`src/limpia_texto.py`)**: Procesa los archivos de texto en `data/textos_limpios/` para eliminar caracteres no deseados, duplicados y normalizar el formato.
3.  **`chunk_main()` (`src/chunk.py`)**: Toma los textos limpios y los divide en fragmentos más pequeños (chunks) con un solapamiento definido en `config.py`. Los chunks se guardan en `data/chunks/todos_los_chunks.json`.
4.  **`embed_main()` (`src/embed_text.py`)**: Carga los chunks y utiliza el modelo `all-MiniLM-L6-v2` para crear un embedding para cada uno. Estos embeddings se almacenan en una colección de ChromaDB llamada `normativa_andalucia` en el directorio `data/chunks/`.
