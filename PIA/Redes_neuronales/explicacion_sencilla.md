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

**Paso 1: Limpieza (Quitar lo raro)**
Primero, tiramos a la basura las casas que son demasiado caras o demasiado baratas para que no "contaminen" el aprendizaje. Nos quedamos con las casas normales.

**Paso 2: Inventar una pista nueva**
Le dimos una pista extra al niño: "¿Ha sido reformada la casa recientemente?". Si el año de reforma es más nuevo que el de construcción, el niño anota un "sí".

**Paso 3: El examen (Dos modelos)**
- **Modelo A (El vago):** Solo mira cuántas habitaciones tiene la casa. Acierta un poco, pero se equivoca bastante.
- **Modelo B (El aplicado):** Mira las habitaciones, los baños (completos y aseos) y si está reformada. Al tener más pistas, sus "adivinanzas" son mucho más precisas.

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
