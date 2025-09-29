'''
Redacta un programa en Python que modele con grafos el mapa de carreteras de algunas ciudades de la provincia de cádiz teniendo en cuenta la distancia kilométrica entre las mismas.
El programa debe permitir mostrar, dada una ciudad, a que otras ciudades se puede llegar y su distancia
'''
class Grafo:
    def __init__(self, num_vertices):
        self.V = num_vertices
        self.grafo = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]

    def agregar_arista(self, u, v, distancia):
        self.grafo[u][v] = distancia
        self.grafo[v][u] = distancia  # Grafo no dirigido

    def mostrar_conexiones(self, ciudad, nombres):
        print(f"\nDesde {nombres[ciudad]} puedes ir a:")
        for i in range(self.V):
            if self.grafo[ciudad][i] != 0:
                print(f"  - {nombres[i]} a {self.grafo[ciudad][i]} km")

if __name__ == "__main__":
    ciudades = ["Cádiz", "Jerez", "San Fernando", "Algeciras", "Chiclana", "El Puerto"]
    g = Grafo(len(ciudades))

    g.agregar_arista(0, 1, 34)   # Cádiz - Jerez
    g.agregar_arista(0, 2, 13)   # Cádiz - San Fernando
    g.agregar_arista(1, 5, 15)   # Jerez - El Puerto
    g.agregar_arista(1, 4, 40)   # Jerez - Chiclana
    g.agregar_arista(1, 3, 110)  # Jerez - Algeciras
    g.agregar_arista(2, 4, 17)   # San Fernando - Chiclana
    g.agregar_arista(4, 3, 100)  # Chiclana - Algeciras

    print("Matriz de adyacencia:")
    for fila in g.grafo:
        for num in fila:
            print(f"{num:4}", end="")
        print()
    
    while True:
        print("\nCiudades disponibles:")
        for i, nombre in enumerate(ciudades):
            print(f"{i}: {nombre}")
        opcion = input("Elige una ciudad por número (o 'salir'): ")

        if opcion.lower() == "salir":
            break

        if opcion.isdigit() and 0 <= int(opcion) < len(ciudades):
            g.mostrar_conexiones(int(opcion), ciudades)
        else:
            print("Opción no válida")
