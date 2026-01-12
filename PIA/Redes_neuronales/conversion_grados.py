import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor

# 1. Crear datos de entrenamiento (Celsius y Fahrenheit)
# Formula: F = C * 1.8 + 32
celsius = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float).reshape(-1, 1)
fahrenheit = np.array([-40, 14, 32, 46.4, 59, 71.6, 100.4], dtype=float)

# 2. Definir el modelo (Red Neuronal)
# Usamos MLPRegressor. Para un problema lineal simple, una "red" pequeña es suficiente.
# Nota: Scikit-learn MLPRegressor está diseñado para problemas más complejos, 
# pero podemos forzarlo a ser simple.
model = MLPRegressor(
    hidden_layer_sizes=(1,), 
    activation='identity', 
    solver='lbfgs', 
    max_iter=1000,
    random_state=42
)

# 3. Entrenar el modelo
print("Entrenando el modelo...")
model.fit(celsius, fahrenheit)
print("Entrenamiento completado.")

# 4. Realizar predicciones
celsius_test = np.array([100, 25, 0]).reshape(-1, 1)
predicciones = model.predict(celsius_test)

print("\nResultados de predicción:")
for c, p in zip(celsius_test.flatten(), predicciones):
    f_real = c * 1.8 + 32
    print(f"Celsius: {c} -> Predicción Fahrenheit: {p:.2f} (Real: {f_real})")

# Ver los coeficientes (pesos)
print(f"\nPeso (Weight): {model.coefs_[0][0][0]:.4f} (Esperado: 1.8)")
print(f"Sesgo (Bias): {model.intercepts_[0][0]:.4f} (Esperado: 32.0)")
