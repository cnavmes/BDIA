
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

print("Cargando librerías y datos...")

# 1. Carga y Limpieza
try:
    df = pd.read_csv('AirQuality.csv', sep=';', decimal=',', skipfooter=114, engine='python')
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    df = df.replace(-200, np.nan)
    df = df.dropna(subset=['NO2(GT)'])
    df = df.fillna(df.median(numeric_only=True))
    print(f"Dimensiones tras limpieza: {df.shape}")

    # 2. Selección de Características (Top 6)
    corr_matrix = df.corr(numeric_only=True)
    target_corr = corr_matrix['NO2(GT)'].abs().sort_values(ascending=False)
    
    # Seleccionamos las 6 mejores (excluyendo la propia variable objetivo que es la 0)
    features = target_corr.index[1:7].tolist()
    print(f"Características seleccionadas (Top 6): {features}")
    
    # 3. Preparación
    X = df[features]
    y = df['NO2(GT)']
    
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_raw)
    X_test = scaler.transform(X_test_raw)
    
    # 4. Modelo
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(32, activation='relu'),
        Dense(16, activation='relu'),
        Dense(1)
    ])
    
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error', metrics=['mae'])
    
    print("Entrenando modelo con 6 variables...")
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=0)
    
    # 5. Evaluación
    test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nResultados con 6 variables:")
    print(f"Error Medio Absoluto (MAE) final: {test_mae:.2f}")
    
    preds = model.predict(X_test[:10])
    print("\nEjemplos:")
    for p, r in zip(preds, y_test[:10]):
        print(f"Pred: {p[0]:.2f} | Real: {r:.2f}")

except Exception as e:
    print(f"Ocurrió un error: {e}")
