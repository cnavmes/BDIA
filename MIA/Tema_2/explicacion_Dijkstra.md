
# 1) Código (para referencia)

```python
import heapq

def dijkstra(grafo, inicio):
    # Distancias iniciales: infinito para todos menos el nodo de inicio
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    
    # Cola de prioridad: (distancia, nodo)
    cola = [(0, inicio)]
    
    while cola:
        dist_actual, nodo_actual = heapq.heappop(cola)
        
        # Si ya encontramos un camino mejor antes, lo ignoramos
        if dist_actual > distancias[nodo_actual]:
            continue
        
        # Recorremos los vecinos del nodo actual
        for vecino, peso in grafo[nodo_actual].items():
            nueva_dist = dist_actual + peso
            
            # Si encontramos un camino más corto, lo actualizamos
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                heapq.heappush(cola, (nueva_dist, vecino))
    
    return distancias
```

# 2) Explicación línea a línea

* `import heapq`
  Importa el módulo que implementa un *heap* (montículo). Con él usaremos una **cola de prioridad** donde siempre extraemos el elemento con menor `distancia` en `O(log n)` por inserción/extracción.

* `def dijkstra(grafo, inicio):`
  Función que recibe:

  * `grafo`: representación como **diccionario de adyacencia**, p.ej. `{'A': {'B':4, 'C':2}, 'B': {'A':4, 'D':1}, ...}`.
  * `inicio`: nodo desde el que calculamos distancias.

* `distancias = {nodo: float('inf') for nodo in grafo}`
  Inicializamos un diccionario con la **distancia conocida** desde `inicio` a cada nodo. Al principio todo es infinito (desconocido).

* `distancias[inicio] = 0`
  La distancia del nodo origen a sí mismo es 0.

* `cola = [(0, inicio)]`
  La cola de prioridad (heap) contiene tuplas `(distancia, nodo)`. Se pone la tupla porque `heapq` ordena por el primer elemento de la tupla — así siempre sacamos el nodo con menor distancia conocida.

* `while cola:`
  Repetimos mientras haya nodos por procesar en la cola.

* `dist_actual, nodo_actual = heapq.heappop(cola)`
  Sacamos (y eliminamos) de la cola el par con menor `distancia` (la raíz del heap).

* `if dist_actual > distancias[nodo_actual]: continue`
  **Clave práctica:** cuando actualizamos la distancia de un nodo, metemos en la cola otra tupla con la nueva distancia. Eso genera entradas duplicadas antiguas (con distancia mayor) que aún pueden estar en la cola. Si al extraer vemos que la distancia extraída `dist_actual` es **mayor** que la distancia ya mejorada en `distancias[nodo_actual]`, esa entrada está obsoleta y la ignoramos.

* `for vecino, peso in grafo[nodo_actual].items():`
  Recorremos todos los vecinos (adyacentes) del `nodo_actual` y el peso de la arista hacia cada vecino.

* `nueva_dist = dist_actual + peso`
  Distancia candidata desde **inicio** pasando por `nodo_actual` hasta `vecino`.

* `if nueva_dist < distancias[vecino]:`
  Si esa distancia es mejor que la actual, actualizamos:

  * `distancias[vecino] = nueva_dist` — guardamos la nueva mejor distancia.
  * `heapq.heappush(cola, (nueva_dist, vecino))` — metemos la nueva tupla en la cola. (Puede coexistir con la antigua; la antigua será ignorada cuando salga.)

* `return distancias`
  Devuelve el diccionario con la distancia mínima desde `inicio` a cada nodo. Si un nodo no es alcanzable, permanecerá `float('inf')`.

# 3) Trazado paso a paso (ejemplo)

Usamos el grafo:

```
A --4-- B
| \     |
2  5    1
|    \  |
C --8-- D
```

Representación:

```python
grafo = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'D': 1},
    'C': {'A': 2, 'D': 8},
    'D': {'B': 1, 'C': 8}
}
```

Inicialmente:

* `distancias = {A:0, B:inf, C:inf, D:inf}`
* `cola = [(0, 'A')]`

Iteración 1:

* Pop `(0, 'A')`.
* Vecinos: B (peso 4) → `nueva_dist = 0+4 = 4` → `dist[B] = 4`, push `(4,'B')`.
  C (peso 2) → `nueva_dist = 2` → `dist[C] = 2`, push `(2,'C')`.
* Cola ahora: `[(2,'C'), (4,'B')]`

Iteración 2:

* Pop `(2,'C')` (es el menor).
* Vecinos: A (2) → `2+2=4` > `dist[A]=0` → ignorado.
  D (8) → `2+8=10` < inf → `dist[D]=10`, push `(10,'D')`.
* Cola: `[(4,'B'), (10,'D')]`

Iteración 3:

* Pop `(4,'B')`.
* Vecinos: A (4) → `4+4=8` > `dist[A]=0` → ignorado.
  D (1) → `4+1=5` < `dist[D]=10` → `dist[D]=5`, push `(5,'D')`.
* Cola: `[(5,'D'), (10,'D')]`

Iteración 4:

* Pop `(5,'D')`.
* Recorremos vecinos: no mejora nada.
* Cola: `[(10,'D')]`

Iteración 5:

* Pop `(10,'D')`. Pero `10 > distancias['D'] (5)`, así que `continue` (entrada obsoleta).
* Cola vacía → terminamos.

Resultado final: `{'A':0, 'B':4, 'C':2, 'D':5}`

# 4) Notas, matices y mejoras

* **Por qué usar `(dist, nodo)` en la cola:** `heapq` compara por el primer elemento de la tupla; así el heap mantiene el mínimo por distancia. Si hay empate en distancia, compara el nodo (no importa mucho normalmente).

* **Duplicados en la cola:** El algoritmo no intenta "decrement-key" en el heap (operación que no existe en `heapq`); en su lugar se insertan nuevos pares y se ignoran las entradas obsoletas con `if dist_actual > distancias[...]`.

* **¿Se puede usar un `visited`?** Sí. Otra variante marca un nodo como `visitado` la primera vez que se extrae (esa distancia es definitiva) y luego se ignoran entradas del mismo nodo futuras. Ambas estrategias funcionan; la de comprobar `dist_actual > distancias[...]` es suficiente y segura.

* **Complejidad:**

  * Tiempo: (O((V + E)\log V)). En grafos conectados y densos suele expresarse como (O(E \log V)).
  * Espacio: (O(V)) adicional (para `distancias`, la cola y opcionalmente `prev`).

* **Peso negativo:** Dijkstra **NO** funciona si hay aristas de peso negativo. Para eso hay que usar Bellman–Ford u otros algoritmos.

* **Nodos no listados en claves:** Asegúrate de que `grafo` incluya como clave todos los nodos (si un nodo no tiene aristas salientes, su valor debería ser `{}`), para que `distancias` lo incluya.

# 5) Variante: reconstruir caminos (no solo distancias)

Si quieres además el camino más corto, guarda el antecesor cuando actualizas:

```python
import heapq

def dijkstra_con_camino(grafo, inicio):
    dist = {n: float('inf') for n in grafo}
    prev = {n: None for n in grafo}
    dist[inicio] = 0
    heap = [(0, inicio)]
    
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in grafo[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev

def reconstruir(prev, inicio, destino):
    path = []
    cur = destino
    while cur is not None:
        path.append(cur)
        if cur == inicio:
            break
        cur = prev[cur]
    path.reverse()
    if path[0] != inicio:
        return None  # no hay camino
    return path
```

Ejemplo de uso:

```python
dist, prev = dijkstra_con_camino(grafo, 'A')
print(dist['D'])                 # 5
print(reconstruir(prev, 'A', 'D'))  # ['A', 'B', 'D']
```

---


