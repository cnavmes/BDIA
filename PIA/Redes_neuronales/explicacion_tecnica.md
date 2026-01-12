# Documentación Técnica: Redes Neuronales Regresoras 🛠️📊

Este documento detalla el flujo técnico seguido para la implementación de los modelos de regresión mediante Redes Neuronales (MLP - Multi-Layer Perceptron) usando la librería `scikit-learn`.

---

## 1. Conversión de Temperaturas (Regresión Simple)

El objetivo es que la red aprenda la función lineal $f(x) = wx + b$.

### Pasos Técnicos:
1.  **Preparación de Tensores**: Se definen los datos en arrays de `numpy`. Es crucial el uso de `.reshape(-1, 1)` para que la entrada sea una matriz de una sola columna, tal como espera el modelo.
2.  **Arquitectura del Modelo**:
    -   `hidden_layer_sizes=(1,)`: Una única neurona, ya que es una relación lineal simple.
    -   `activation='identity'`: No aplicamos funciones no lineales (como ReLU) porque queremos una salida lineal directa.
    -   `solver='lbfgs'`: Un optimizador cuasi-Newton ideal para datasets pequeños, ya que converge más rápido que el descenso de gradiente estocástico (SGD) en estos casos.
3.  **Extracción de Parámetros**: Al finalizar, extraemos `coefs_` (pesos) e `intercepts_` (sesgo) para verificar que coincidan con 1.8 y 32 respectivamente.

---

## 2. Predicción de Precios de Viviendas (Pipeline Completo)

Siguiendo el temario avanzado, hemos estructurado el proceso en bloques pedagógicos:

### Bloque 1 & 2: Comprensión y Correlación
- **EDA (Exploratory Data Analysis)**: Usamos `info()` y `describe()` para identificar el tipo de variables (numéricas vs categóricas) y sus escalas.
- **Matriz de Correlación**: Calculada con `df.corr()`. Nos permite ver qué variables tienen mayor impacto lineal sobre el `SalePrice` (ej: `OverallQual`, `GrLivArea`).
  - *Resultado*: Se genera `correlation_matrix.png`.

### Bloque 3 & 4: Limpieza y Tratamiento
- **Valores Nulos**: Implementamos imputación mediante la mediana (`fillna(df.median())`) para asegurar que la red neuronal reciba datos completos.
- **Tratamiento de Outliers**: Mantenemos el filtrado por percentiles (10-90) para eliminar ruidos extremos que dificulten el aprendizaje de la red.

### Bloque 5 & 7: Transformación y Codificación
- **Ingeniería de Variables**: Creación de la columna `reformada`.
- **Clasificación Auxiliar**: Para demostrar el uso de una **Matriz de Confusión**, categorizamos el precio en 3 niveles (Bajo, Medio, Alto) usando `pd.qcut`.

### Bloque 6 & 8: Escalado y Partición
- **StandardScaler**: Transformamos las características para que tengan media 0 y varianza 1. Sin esto, la red no converge correctamente debido a la diferencia de escalas entre "habitaciones" (0-10) y "metros cuadrados" (0-5000).
- **Train/Test Split**: División 80/20 para evitar el *Data Leakage* y validar el rendimiento real.

### Bloque 10: Evaluación y Matrices
1. **Regresión**: Evaluamos con MAE y RMSE para medir la precisión en dólares.
2. **Clasificación**: Entrenamos un `MLPClassifier` para predecir la categoría de precio.
   - **Matriz de Confusión**: Generamos `confusion_matrix.png` para visualizar dónde el modelo confunde una categoría con otra.

---

### Stack Tecnológico
- **Python 3.12**
- **Pandas & NumPy**: Procesamiento de datos.
- **Scikit-Learn**: Modelos `MLPRegressor` y `MLPClassifier`.
- **Matplotlib**: Generación de visualizaciones gráficas.
