# Interpretación de los Resultados 📊🏠

Tras ejecutar el modelo multivariable, hemos obtenido unas métricas que nos dicen qué tan bien (o mal) está "adivinando" nuestra red neuronal. Aquí tienes el análisis:

---

## 1. Regresión (Predicción de Precio en $)

**Variables usadas:** Habitaciones, Baños completos, Aseos y si está reformada.

- **MAE (Error Medio Absoluto): ~$28,000**
  - **¿Qué significa?** En promedio, el precio que dice la IA se desvía unos 28k dólares del precio real. 
  - **¿Es bueno?** Para haber usado solo **4 pistas** de las 81 disponibles en el dataset, es un resultado **aceptable**. 

- **MAPE (Error Porcentual): ~16%**
  - **¿Qué significa?** Es el error relativo al precio. Si una casa vale $100,000, el modelo fallará de media unos $16,000.
  - **¿Cómo interpretarlo?** Es la forma más fácil de entender la precisión. Un 16% de error significa que el modelo tiene una "puntería" del 84%. Para ser un modelo con solo 4 variables, está muy bien.
  
- **RMSE (Raíz del Error Cuadrático Medio): ~$37,000**
  - **¿Qué significa?** Es mayor que el MAE porque esta métrica "castiga" más fuerte los fallos grandes. Si una casa de lujo la predice como barata, el RMSE sube mucho.

---

## 2. Clasificación (Categorías: Bajo, Medio, Alto)

Hemos dividido las casas en tres grupos iguales por precio. La **Matriz de Confusión** nos dice dónde se lía el modelo:

- **Casas Baratas (Bajo)**: Acierta **63 de 93**. ¡Bastante bien! Sabe identificar las casas económicas con facilidad.
- **Casas Caras (Alto)**: Acierta **53 de 67**. ¡Muy bien (~79%)! Las casas de lujo suelen tener muchas habitaciones y baños, por lo que el modelo no tiene dudas.
- **Casas Intermedias (Medio)**: Aquí es donde más falla. Acierta **29 de 74**. Muchas casas "normales" las confunde con "caras" (30 veces).
  - **Conclusión**: El modelo es bueno detectando los extremos (lo muy barato y lo muy caro), pero le cuesta diferenciar una casa de clase media de una un poco más lujosa solo con el número de habitaciones.

---

## 3. Veredicto Final: ¿Es un buen modelo? 🤔

1. **Para un ejercicio de clase**: **Sobresaliente**. Has demostrado que un algoritmo puede aprender patrones de precio con muy poca información.
2. **Para uso real (Profesional)**: **Insuficiente**. Un error de $28,000 es demasiado margen para un comprador o vendedor.
3. **¿Cómo mejorar?**: Según tu temario (Bloque 2 y 7), la clave sería añadir la variable `GrLivArea` (superficie habitable), que suele tener la mayor correlación con el precio.

**En resumen**: Tu red neuronal ya "entiende" que más habitaciones = más caro, pero aún no sabe distinguir si esas habitaciones están en un barrio de lujo o en la periferia. 🚀
