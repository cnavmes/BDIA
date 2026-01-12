import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import StandardScaler

# ==========================================
# BLOQUE 1 & 2: COMPRENSIÓN Y EXPLORACIÓN
# ==========================================
print("--- Bloque 1: Comprensión del Dataset ---")
file_path = "train.csv"
df = pd.read_csv(file_path)

# 1.1. Información general (Tipos de variables)
print("\nInformación del Dataset:")
df.info()

# 1.2. Análisis estadístico (Rangos y escalas)
print("\nDescripción Estadística:")
print(df[['SalePrice', 'TotRmsAbvGrd', 'FullBath', 'HalfBath', 'YearBuilt', 'YearRemodAdd']].describe())

# 2.2. Matriz de Correlación
print("\n--- Bloque 2: Análisis de Correlación ---")
# Solo columnas numéricas para correlación
numeric_df = df.select_dtypes(include=[np.number])
correlation_matrix = numeric_df.corr()
print("\nCorrelación con SalePrice (Top 10):")
print(correlation_matrix['SalePrice'].sort_values(ascending=False).head(10))

# Guardar matriz de correlación como imagen
plt.figure(figsize=(12, 10))
plt.matshow(correlation_matrix, fignum=1)
plt.colorbar()
plt.title("Matriz de Correlación", pad=20)
plt.savefig("correlation_matrix.png")
print("\nMatriz de correlación guardada como 'correlation_matrix.png'")

# ==========================================
# BLOQUE 3 & 4: LIMPIEZA Y OUTLIERS
# ==========================================
print("\n--- Bloque 3: Tratamiento de Valores Nulos ---")
null_counts = df[['TotRmsAbvGrd', 'FullBath', 'HalfBath', 'YearBuilt', 'YearRemodAdd']].isnull().sum()
print(f"Valores nulos detectados:\n{null_counts}")

# Imputación simple (en este caso no hay nulos en estas columnas, pero dejamos el código por pedagogía)
df['FullBath'] = df['FullBath'].fillna(df['FullBath'].median())

print("\n--- Bloque 4: Detección de Outliers ---")
# Filtramos por percentiles 10 y 90 para SalePrice (como pidió el usuario originalmente)
lower_bound = df['SalePrice'].quantile(0.10)
upper_bound = df['SalePrice'].quantile(0.90)
filtered_df = df[(df['SalePrice'] >= lower_bound) & (df['SalePrice'] <= upper_bound)].copy()
print(f"Registros originales: {len(df)} -> Filtrados: {len(filtered_df)}")

# ==========================================
# BLOQUE 5 & 7: TRANSFORMACIÓN Y CODIFICACIÓN
# ==========================================
print("\n--- Bloque 7: Feature Engineering ---")
# Crear variable 'reformada'
filtered_df['reformada'] = (filtered_df['YearRemodAdd'] > filtered_df['YearBuilt']).astype(int)

# Crear categorías para Clasificación (Sub-tarea para Matriz de Confusión)
# Dividimos el precio en 3 categorías: Bajo, Medio, Alto
filtered_df['PriceCategory'] = pd.qcut(filtered_df['SalePrice'], 3, labels=[0, 1, 2]) # 0: Bajo, 1: Medio, 2: Alto

# ==========================================
# BLOQUE 6 & 8: ESCALADO Y PARTICIÓN
# ==========================================
print("\n--- Bloque 6 & 8: Escalado y Partición ---")
X = filtered_df[['TotRmsAbvGrd', 'FullBath', 'HalfBath', 'reformada']]
y_reg = filtered_df['SalePrice']
y_clf = filtered_df['PriceCategory']

# División para Regresión
X_train, X_test, y_train_reg, y_test_reg = train_test_split(X, y_reg, test_size=0.2, random_state=42)
# División para Clasificación (usamos los mismos índices para consistencia)
_, _, y_train_clf, y_test_clf = train_test_split(X, y_clf, test_size=0.2, random_state=42)

# Escalado (Crítico para Redes Neuronales)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==========================================
# BLOQUE 10 & 12: MODELADO Y EVALUACIÓN
# ==========================================
print("\n--- Bloque 10: Modelado (Regresión) ---")
reg_model = MLPRegressor(hidden_layer_sizes=(20, 20), max_iter=3000, random_state=42)
reg_model.fit(X_train_scaled, y_train_reg)

preds_reg = reg_model.predict(X_test_scaled)
mae = mean_absolute_error(y_test_reg, preds_reg)
rmse = np.sqrt(mean_squared_error(y_test_reg, preds_reg))
print(f"Regresión - MAE: ${mae:.2f}")
print(f"Regresión - RMSE: ${rmse:.2f}")

print("\n--- Bloque 10: Modelado (Clasificación para Confusión) ---")
clf_model = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=2000, random_state=42)
clf_model.fit(X_train_scaled, y_train_clf)

preds_clf = clf_model.predict(X_test_scaled)
cm = confusion_matrix(y_test_clf, preds_clf)

# Mostrar y guardar Matriz de Confusión
print("Matriz de Confusión (Categorías de Precio):")
print(cm)

plt.figure(figsize=(8, 6))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Bajo", "Medio", "Alto"])
disp.plot(cmap=plt.cm.Blues)
plt.title("Matriz de Confusión: Categorías de Precio")
plt.savefig("confusion_matrix.png")
print("\nMatriz de confusión guardada como 'confusion_matrix.png'")

# ==========================================
# PARTE FINAL: PREDICCIÓN EN TEST.CSV
# ==========================================
print("\n--- Generando predicciones finales para test.csv ---")
test_df = pd.read_csv("test.csv")

# Aplicar las mismas transformaciones
test_df['reformada'] = (test_df['YearRemodAdd'] > test_df['YearBuilt']).astype(int)

# Manejar nulos en test (importante para que no falle el modelo)
test_df['FullBath'] = test_df['FullBath'].fillna(test_df['FullBath'].median())
test_df['HalfBath'] = test_df['HalfBath'].fillna(test_df['HalfBath'].median())
test_df['TotRmsAbvGrd'] = test_df['TotRmsAbvGrd'].fillna(test_df['TotRmsAbvGrd'].median())

X_test_final = test_df[['TotRmsAbvGrd', 'FullBath', 'HalfBath', 'reformada']]
X_test_final_scaled = scaler.transform(X_test_final)

final_preds = reg_model.predict(X_test_final_scaled)

output = pd.DataFrame({'Id': test_df['Id'], 'SalePrice_Predicted': final_preds})
output.to_csv("predicciones_casas.csv", index=False)
print("Archivo 'predicciones_casas.csv' actualizado exitosamente.")
