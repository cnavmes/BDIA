import random

def simular_extraccion(num_repeticiones = 100000):

    bolas = ["negra" for _ in range(5)] + ["blanca" for _ in range(7)]
    exitos = 0

    for _ in range(num_repeticiones):
        bolas_extraidas = random.sample(bolas,4)
        if bolas_extraidas.count("negra") == 4:
            exitos += 1

    probabilidad = exitos / num_repeticiones
    return probabilidad

probabilidad_de_exito = simular_extraccion() * 100

print(f"La probabilidad es de : {probabilidad_de_exito} %")

#Combinatoria

import math

def combinaciones(n, k):
    return math.comb(n, k)

bolas_negras = 5
bolas_blancas = 7
total_bolas = 12
bolas_extraidas = 4

# Calcular combinaciones
formas_negras = combinaciones(bolas_negras, 4)
formas_blancas = combinaciones(bolas_blancas, 0)
formas_totales = combinaciones(total_bolas, 4)

# Probabilidad
probabilidad = (formas_negras * formas_blancas) / formas_totales
print(f'Probabilidad exacta de extraer 4 bolas negras: {probabilidad:.6f}')
