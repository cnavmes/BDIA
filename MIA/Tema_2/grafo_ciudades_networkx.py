import networkx as nx

ciudades = ["Cádiz", "Jerez", "San Fernando", "Algeciras", "Chiclana", "El Puerto"]

distancias = {
    ("Cádiz", "Jerez"): 34,
    ("Cádiz", "San Fernando"): 13,
    ("Jerez", "El Puerto"): 15,
    ("Jerez", "Chiclana"): 40,
    ("Jerez", "Algeciras"): 110,
    ("San Fernando", "Chiclana"): 17,
    ("Chiclana", "Algeciras"): 100
}

G = nx.Graph()
for (c1, c2), d in distancias.items():
    G.add_edge(c1, c2, weight=d)

def mostrar_conexiones(grafo, ciudad):
    print(f"\nDesde {ciudad} puedes ir a:")
    for vecino in grafo[ciudad]:
        distancia = grafo[ciudad][vecino]["weight"]
        print(f"  - {vecino} a {distancia} km")


while True:
    print("\nCiudades disponibles:")
    for i, nombre in enumerate(ciudades):
        print(f"{i}: {nombre}")
    
    opcion = input("Elige una ciudad por número (o escribe 'salir' para terminar): ")
    
    if opcion.lower() == "salir":
        break
    
    if opcion.isdigit() and 0 <= int(opcion) < len(ciudades):
        ciudad_elegida = ciudades[int(opcion)]
        mostrar_conexiones(G, ciudad_elegida)
    else:
        print("Opción no válida")