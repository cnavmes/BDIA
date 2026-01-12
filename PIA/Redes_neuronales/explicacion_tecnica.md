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

## 2. Predicción de Precios de Viviendas (Regresión Multivariable)

### Pasos Técnicos:

#### A. Preprocesamiento y Limpieza
1.  **Tratamiento de Outliers (Valores Atípicos)**:
    -   Se utilizan los cuantiles 0.10 y 0.90 de la variable `SalePrice`.
    -   *Razón*: Las redes neuronales son sensibles a valores extremos que pueden sesgar el aprendizaje de los pesos.
2.  **Ingeniería de Características (Feature Engineering)**:
    -   Creación de `reformada`: Variable booleana transformada a entero (0 o 1). Compara `YearRemodAdd` vs `YearBuilt`.

#### B. Preparación para el Entrenamiento
1.  **División del Dataset**: Uso de `train_test_split` (80% entrenamiento, 20% validación). Es vital para evaluar la capacidad de generalización y detectar el *overfitting*.
2.  **Escalado de Características (StandardScaler)**:
    -   **CRUCIAL**: Las redes neuronales utilizan algoritmos basados en gradiente. Si una variable tiene un rango de 0-10 (habitaciones) y otra de 0-200.000 (precio), la red tardará mucho en converger o fallará.
    -   `StandardScaler` normaliza los datos para que tengan media 0 y desviación típica 1.

#### C. Arquitectura y Entrenamiento
1.  **Modelo B (Multivariable)**:
    -   `hidden_layer_sizes=(20, 20)`: Red con dos capas ocultas de 20 neuronas cada una. Esto permite capturar interacciones complejas entre variables (ej: cómo influyen los baños si la casa es reformada).
    -   `max_iter=3000`: Se aumenta el límite de iteraciones para permitir que el optimizador encuentre el mínimo global de la función de pérdida.

#### D. Evaluación y Predicción Final
1.  **Métricas de Error**:
    -   **MAE (Error Medio Absoluto)**: Promedio de las desviaciones en dólares. Muy interpretable.
    -   **RMSE (Raíz del Error Cuadrático Medio)**: Penaliza más los errores grandes.
2.  **Inferencia en Test Set**:
    -   Se aplican las **mismas transformaciones** al archivo `test.csv` (ingeniería de variables y escalado usando el *scaler* ya entrenado).
    -   Los resultados se exportan a `predicciones_casas.csv`.

---

### Stack Tecnológico
-   **Python 3.12**
-   **Pandas**: Manipulación de datos estructurados.
-   **Scikit-Learn**: Implementación del `MLPRegressor` y preprocesamiento.
-   **NumPy**: Operaciones matriciales eficientes.
