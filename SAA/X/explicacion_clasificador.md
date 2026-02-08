# Explicación del Clasificador de Productos

Este script implementa un clasificador de sentimiento básico utilizando Procesamiento de Lenguaje Natural (NLP) y aprendizaje automático (Machine Learning).

## Paso 1: Importación de Librerías y Recursos
El código utiliza `nltk` para el manejo de texto (tokenización y stopwords) y `sklearn` para la vectorización y el modelo de Naive Bayes.
- **`nltk.download(...)`**: Descarga los paquetes necesarios para separar frases en palabras (`punkt`, `punkt_tab`) y filtrar palabras comunes (`stopwords`).

## Paso 2: Función de Preprocesamiento (`preprocesar_texto`)
Esta es la fase de limpieza de los datos para que el modelo no se distraiga con ruido:
1.  **Conversión a minúsculas**: Para que "Excelente" y "excelente" se traten como la misma palabra.
2.  **Tokenización**: Divide la frase en una lista de palabras individuales (tokens).
3.  **Filtrado de Stopwords (Personalizado)**:
    - Las *stopwords* son palabras comunes (artículos, preposiciones) que no suelen aportar significado temático.
    - **Detalle clave**: El código quita palabras de negación (como "no", "ni", "sin", "pero") de la lista de eliminación. Esto es vital porque en análisis de sentimiento, la palabra "no" cambia totalmente el sentido de la frase (ej: "no es bueno").
4.  **Limpieza Alfanumérica**: Se eliminan signos de puntuación y símbolos, dejando solo palabras y números.

## Paso 3: Definición del Dataset
Se define `data_valoraciones`, una lista de ejemplos etiquetados:
- **Entrada**: Comentarios reales ("Increíble producto", "No funciona").
- **Salida (Etiqueta)**: La categoría a la que pertenecen ("buena valoracion" o "mala valoracion").

## Paso 4: Preparación y Vectorización
Las máquinas solo entienden números, por lo que debemos convertir el texto:
1.  **Limpieza en masa**: Se aplica la función de preprocesamiento a todos los textos de entrenamiento.
2.  **`CountVectorizer`**: Convierte los textos en una "Bolsa de Palabras" (Bag of Words). Crea una matriz donde cada columna es una palabra del vocabulario y cada celda indica cuántas veces aparece esa palabra en un comentario específico.

## Paso 5: Entrenamiento del Modelo (`MultinomialNB`)
Se entrena un clasificador de **Naive Bayes Multinomial**. Este algoritmo calcula probabilidades: ¿Qué tan probable es que un comentario sea "malo" si contiene la palabra "basura"? 
- El modelo "aprende" las asociaciones entre palabras y sentimientos basándose en los ejemplos proporcionados.

## Paso 6: Función de Clasificación (`clasificar_comentario`)
Es la función que permite usar el sistema con datos nuevos:
1.  Recibe un comentario del usuario.
2.  Lo preprocesa para que tenga el mismo formato que los datos de entrenamiento.
3.  Lo transforma en números usando el vectorizador ya entrenado.
4.  Pide al modelo que realice una predicción.

## Paso 7: Bucle Interactivo
Al ejecutar el archivo directamente, se activa un menú en la terminal:
- Permite al usuario introducir cualquier texto.
- Muestra la predicción en mayúsculas.
- Permite salir escribiendo 'salir', 'exit' o 'quit'.
