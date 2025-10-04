import networkx as nx
import matplotlib.pyplot as plt

# Diccionario con distancias
distancias = {
    ("Cádiz", "Jerez"): 34,
    ("Cádiz", "San Fernando"): 13,
    ("Jerez", "El Puerto"): 15,
    ("Jerez", "Chiclana"): 40,
    ("Jerez", "Algeciras"): 110,
    ("San Fernando", "Chiclana"): 17,
    ("Chiclana", "Algeciras"): 100
}

# Crear grafo
G = nx.Graph()
for (origen, destino), peso in distancias.items():
    G.add_edge(origen, destino, weight=peso)

inicio = input("Introduce la ciudad de origen: ")

if inicio not in G:
    print(f"La ciudad {inicio} no está en el grafo.")
else:
    # Distancias y rutas separadas
    rutas = nx.single_source_dijkstra_path(G, inicio, weight='weight')
    distancias_minimas = nx.single_source_dijkstra_path_length(G, inicio, weight='weight')

    print(f"\nCaminos más cortos desde {inicio}:\n")
    for ciudad, ruta in rutas.items():
        print(f"{inicio} -> {ciudad}: {ruta}, distancia = {distancias_minimas[ciudad]} km")

    # Dibujar grafo
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

    # Resaltar rutas desde el origen
    for destino, ruta in rutas.items():
        if destino == inicio:
            continue
        aristas_ruta = list(zip(ruta[:-1], ruta[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=aristas_ruta, edge_color='red', width=3)

    plt.title(f"Caminos más cortos desde {inicio}")
    plt.show()
