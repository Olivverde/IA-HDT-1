from queue import PriorityQueue


class Graph:
    def __init__(self, A):
        self.v = A
        self.edges = [[-1 for i in range(A)] for j in range(A)]
        self.visited = []

        def add_edge(self, u, v, weight):
            self.edges[u][v] = weight
            self.edges[v][u] = weight

    def dijkstra(graph, start_vertex):
        D = {v:float('inf') for v in range(graph.v)}
        D[start_vertex] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)

        for neighbor in range(graph.v):
            if graph.edges[current_vertex][neighbor] != -1:
                distance = graph.edges[current_vertex][neighbor]
                if neighbor not in graph.visited:
                    O = D[neighbor]
                    N = D[current_vertex] + distance
                    if N < O:
                        pq.put((N, neighbor))
                        D[neighbor] = N

    return D

        
