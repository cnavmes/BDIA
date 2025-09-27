import networkx as nx

def crear_grafo():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 3)])
    return G

def dfs(G, start):
    for node in nx.dfs_preorder_nodes(G, source=start):
        print(node, end=' ')

def bfs(G, start):
    for node in nx.bfs_preorder_nodes(G, source=start):
        print(node, end=' ')

if __name__ == "__main__":
    G = crear_grafo()

    print("Recorrido en profundidad (comenzando en el vértice 2):")
    dfs(G, 2)
    print("\nRecorrido en anchura (comenzando en el vértice 2):")
    bfs(G, 2)
