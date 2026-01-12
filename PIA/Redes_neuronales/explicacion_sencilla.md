# Explicación Sencilla de lo que hemos hecho 🧠🏡🌡️

Si no sabes nada de Inteligencia Artificial ni de programación, aquí te explico lo que hemos hecho como si se lo contara a mi abuela.

---

## 1. El termómetro inteligente 🌡️

Imagina que tienes a un niño que no sabe matemáticas. Le das una lista de parejas de números:
- -40°C es -40°F
- 0°C es 32°F
- 100°C es 212°F

El niño no conoce la fórmula ($F = 1.8 \times C + 32$), pero después de mirar la lista muchas veces, empieza a "adivinar" el patrón.

**Lo que hizo la Red Neuronal:**
- Empezó adivinando al azar.
- Cada vez que fallaba, se corregía a sí misma ("uy, me pasé", "uy, me quedé corto").
- Al final, ella sola descubrió que tenía que multiplicar por 1.8 y sumar 32, ¡sin que nadie le dijera la regla!

---

## 2. El tasador de casas 🏠

Esto es un poco más difícil. Queremos saber cuánto vale una casa, pero hay casas muy raras que confunden al niño (mansiones de lujo o casas en ruinas).

**Paso 1: Detectar las mejores pistas (Correlación)**
Antes de empezar, el niño mira cuáles son las pistas que más ayudan. Descubre que el tamaño de la casa y la calidad general son los "chivatos" más fiables para saber el precio.

**Paso 2: Limpieza (Quitar lo raro y completar huecos)**
- Tiramos las casas demasiado raras (outliers).
- Si a una casa le faltaba el dato de cuántos baños tiene, le ponemos la media de las demás para que el niño no se quede bloqueado (imputación).

**Paso 3: El examen de los colores (Matriz de Confusión)**
Para ver si el niño es bueno, le pedimos que pinte las casas de 3 colores: Verde (Barata), Azul (Normal), Rojo (Cara).
La **Matriz de Confusión** es un cuadro que nos dice cuántas veces el niño pintó de azul una casa que era verde. ¡Así sabemos en qué tipo de casas se equivoca más!

---

## 3. ¿Cómo lo usamos? 🚀

Para que todo esto funcione, hemos hecho lo siguiente:
1. **Preparar los datos:** Como poner las piezas de un puzzle en orden.
2. **Entrenar:** Dejar que la red neuronal practique con los datos de ejemplo (`train.csv`).
3. **Predecir:** Darle una lista de casas nuevas (`test.csv`) de las que no sabemos el precio y dejar que la red diga: "Yo creo que esta vale tanto".

**Al final, hemos guardado todas sus "adivinanzas" en un archivo llamado `predicciones_casas.csv`.**

---

### ¿Cómo ejecuto todo esto? 💻
Solo tienes que escribir `py` seguido del nombre del archivo en la consola:
- `py conversion_grados.py`
- `py prediccion_casas.py`

¡Y listo! La "magia" ocurre sola.
