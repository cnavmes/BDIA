class Grafo:
    def __init__(self, num_vertices):
        self.V = num_vertices
        self.grafo = [[0 for column in range(num_vertices)] for row in range(num_vertices)]

    def agregar_arista(self, u, v):
        self.grafo[u][v] = 1
        #self.grafo[v][u] = 1  # Para grafos no dirigidos

    def dfs_util(self, v, visitados):
        visitados[v] = True
        print(v, end=' ')
        for i in range(self.V):
            if self.grafo[v][i] and not visitados[i]:
                self.dfs_util(i, visitados)

    def dfs(self, v):
        visitados = [False] * self.V
        self.dfs_util(v, visitados)

    def bfs(self, s):
        visitados = [False] * self.V
        cola = []
        cola.append(s)
        visitados[s] = True
        while cola:
            s = cola.pop(0)
            print(s, end=' ')
            for i in range(self.V):
                if self.grafo[s][i] and not visitados[i]:
                    cola.append(i)
                    visitados[i] = True

if __name__ == "__main__":
    g = Grafo(4)
    g.agregar_arista(0, 1)
    g.agregar_arista(0, 2)
    g.agregar_arista(1, 2)
    g.agregar_arista(2, 0)
    g.agregar_arista(2, 3)
    g.agregar_arista(3, 3)

    print("Recorrido en profundidad (comenzando en el vértice 2):")
    g.dfs(2)
    print("\nRecorrido en anchura (comenzando en el vértice 2):")
    g.bfs(2)
    