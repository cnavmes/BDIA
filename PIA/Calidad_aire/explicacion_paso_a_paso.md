# Guía Detallada: Predicción de NO2 con Redes Neuronales

Este documento explica paso a paso la lógica aplicada en el cuaderno `ejercicio_calidad_aire.ipynb`, detallando el **qué** se hace y el **porqué**.

---

## 1. Carga y Preparación de Datos
### ¿Qué hacemos?
Leemos el archivo `AirQuality.csv` indicando explícitamente que el separador es `;` y que los decimales se marcan con `,`. También eliminamos las últimas 114 filas que suelen estar vacías en este dataset.

### ¿Por qué?
*   **Formato Europeo:** Este dataset usa un formato común en Europa donde la coma es el decimal. Si no se indica, Python interpretaría los números como texto.
*   **Limpieza de origen:** Python lee el archivo tal cual, y si hay filas o columnas "fantasma" al final, pueden causar errores matemáticos más adelante.

---

## 2. Limpieza de Valores Faltantes (NaN)
### ¿Qué hacemos?
Sustituimos todos los `-200` por `NaN` (Not a Number). Luego, completamos los huecos vacíos con la **mediana** de cada columna.

### ¿Por qué?
*   **El código de error:** En sensores reales, el `-200` es una marca de error del sensor. Para una red neuronal, `-200` es un número muy grande negativo que destrozaría los cálculos.
*   **Imputación por mediana:** Las redes neuronales no admiten valores vacíos. Usamos la mediana porque es más robusta que la media (no le afectan tanto los valores extremos) para rellenar los huecos.

---

## 3. Estudio de Correlación
### ¿Qué hacemos?
Calculamos una matriz que mide cómo se mueven las variables entre sí. Un valor de `1.0` es una relación perfecta.

### ¿Por qué?
*   **Selección de Características:** Necesitamos saber qué sensores "ven" lo mismo que el sensor de **NO2(GT)**. Si un sensor sube siempre que el NO2 sube, es un buen candidato para ayudar a predecirlo.
*   **Visualización:** El Heatmap nos permite descartar variables que no tienen ninguna relación con nuestro objetivo.

---

## 4. División Train/Test (80/20)
### ¿Qué hacemos?
Separamos los datos: el 80% lo usará la red para estudiar y el 20% lo guardamos bajo llave.

### ¿Por qué?
*   **Evitar el "Examen Memorizado":** Si evaluamos a la red con los mismos datos con los que aprendió, no sabemos si ha aprendido a razonar o simplemente ha memorizado el dataset. El 20% es el "examen final" con datos nunca vistos.

---

## 5. Escalado de Datos (StandardScaler)
### ¿Qué hacemos?
Transformamos todos los números para que tengan una media de 0 y se muevan en un rango pequeño (típicamente entre -3 y 3).

### ¿Por qué?
*   **Equilibrio de fuerzas:** Imagina que una variable se mide en miles y otra en decimales. La red neuronal pensaría que la de miles es "más importante" solo por ser más grande. El escalado pone a todos los sensores en la misma escala de importancia.

---

## 6. La Red Neuronal (Arquitectura)
### ¿Qué hacemos?
Creamos una estructura de capas:
1.  **Capa de entrada:** Recibe tus 3 variables.
2.  **Capas ocultas (`Dense`):** Capas de neuronas que buscan patrones complejos. Usamos activación `ReLU` que ayuda a gestionar la no-linealidad.
3.  **Capa de salida:** Una sola neurona sin activación (regresión pura).

### ¿Por qué?
*   **Densidad:** Las capas `Dense` permiten que cada neurona se conecte con todas las de la capa anterior, permitiendo captar combinaciones complejas de los sensores.
*   **Regresión:** Como queremos predecir un valor numérico (la cantidad de NO2), la salida debe ser un número libre, no una probabilidad de clase.

---

## 7. Entrenamiento y Evaluación
### ¿Qué hacemos?
Usamos el optimizador `Adam` y la función de pérdida `MSE` (Error cuadrático medio). Graficamos la curva de aprendizaje.

### ¿Por qué?
*   **Función de Pérdida:** Es el "castigo" que recibe la red cuando se equivoca. Cuanto más grande es el error, más fuerte es el ajuste que hace `Adam` en los pesos de las neuronas.
*   **Curva de Pérdida:** Si la línea de entrenamiento baja pero la de validación sube, significa que la red está memorizando (Overfitting). Buscamos que ambas bajen juntas.
