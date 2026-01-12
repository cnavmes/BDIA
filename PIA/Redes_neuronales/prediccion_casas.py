import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler

# 1. Cargar el archivo CSV
file_path = "train.csv"
df = pd.read_csv(file_path)

# 2. Filtrar el DataFrame (percentiles 10 y 90 para 'SalePrice')
lower_bound = df['SalePrice'].quantile(0.10)
upper_bound = df['SalePrice'].quantile(0.90)
filtered_df = df[(df['SalePrice'] >= lower_bound) & (df['SalePrice'] <= upper_bound)].copy()

print(f"Datos originales: {len(df)}")
print(f"Datos filtrados (percentil 10-90): {len(filtered_df)}")

# 3. Transformación de datos (Ingeniería de variables)
# - 'reformada': 1 si YearRemodAdd > YearBuilt, else 0
filtered_df['reformada'] = (filtered_df['YearRemodAdd'] > filtered_df['YearBuilt']).astype(int)

# - 'total_baños': FullBath + 0.5 * HalfBath (opcional, pero usemos lo que pidió el usuario)
# El usuario pidió: "número de baños", usaremos FullBath y HalfBath por separado o sumados.
# Para el modelo B usaremos las características solicitadas.

# --- PARTE A: Solo número de habitaciones ---
print("\n--- Parte A: Predicción basada solo en habitaciones ---")
X_a = filtered_df[['TotRmsAbvGrd']]
y = filtered_df['SalePrice']

X_train_a, X_test_a, y_train, y_test = train_test_split(X_a, y, test_size=0.2, random_state=42)

# Escalar los datos (importante para redes neuronales)
scaler_a = StandardScaler()
X_train_a_scaled = scaler_a.fit_transform(X_train_a)
X_test_a_scaled = scaler_a.transform(X_test_a)

model_a = MLPRegressor(hidden_layer_sizes=(10, 10), max_iter=2000, random_state=42)
model_a.fit(X_train_a_scaled, y_train)

pred_a = model_a.predict(X_test_a_scaled)
mae_a = mean_absolute_error(y_test, pred_a)
rmse_a = np.sqrt(mean_squared_error(y_test, pred_a))

print(f"Error Medio Absoluto (MAE): ${mae_a:.2f}")
print(f"Raíz del Error Cuadrático Medio (RMSE): ${rmse_a:.2f}")


# --- PARTE B: Multivariable ---
print("\n--- Parte B: Predicción multivariable (Habitaciones, Baños, Reformada) ---")
# Características: TotRmsAbvGrd, FullBath, HalfBath, reformada
X_b = filtered_df[['TotRmsAbvGrd', 'FullBath', 'HalfBath', 'reformada']]

X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(X_b, y, test_size=0.2, random_state=42)

# Escalar los datos
scaler_b = StandardScaler()
X_train_b_scaled = scaler_b.fit_transform(X_train_b)
X_test_b_scaled = scaler_b.transform(X_test_b)

# Usamos una red un poco más profunda para capturar relaciones multivariables
model_b = MLPRegressor(hidden_layer_sizes=(20, 20), max_iter=3000, random_state=42)
model_b.fit(X_train_b_scaled, y_train_b)

pred_b = model_b.predict(X_test_b_scaled)
mae_b = mean_absolute_error(y_test_b, pred_b)
rmse_b = np.sqrt(mean_squared_error(y_test_b, pred_b))

print(f"Error Medio Absoluto (MAE): ${mae_b:.2f}")
print(f"Raíz del Error Cuadrático Medio (RMSE): ${rmse_b:.2f}")

# --- PARTE C: Predicción en datos de prueba (test.csv) ---
print("\n--- Parte C: Generando predicciones para test.csv ---")
test_file_path = "test.csv"
test_df = pd.read_csv(test_file_path)

# Ingeniería de variables en test set (la misma que en train)
test_df['reformada'] = (test_df['YearRemodAdd'] > test_df['YearBuilt']).astype(int)

# Seleccionar las mismas características que model_b
# IMPORTANTE: No se filtra por percentiles aquí porque necesitamos predicciones para todo el test set
X_test_final = test_df[['TotRmsAbvGrd', 'FullBath', 'HalfBath', 'reformada']]

# Escalar con el scaler_b ya entrenado
X_test_final_scaled = scaler_b.transform(X_test_final)

# Predecir
pred_final = model_b.predict(X_test_final_scaled)

# Guardar resultados
output = pd.DataFrame({
    'Id': test_df['Id'],
    'SalePrice_Predicted': pred_final
})

output_file = "predicciones_casas.csv"
output.to_csv(output_file, index=False)
print(f"Predicciones guardadas en: {output_file}")
print(output.head())
