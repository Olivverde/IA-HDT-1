#BFS
#Extraido de https://www.educative.io/edpresso/how-to-implement-a-breadth-first-search-in-python
G = {
  'A' : ['B','C'],
  'B' : ['D', 'E'],
  'C' : ['F'],
  'D' : [],
  'E' : ['F'],
  'F' : []
}

#Listas
visited = [] 
queue = []     

#Hacemos seguimiento del nodo
def bfs(visited, G, node):
  visited.append(node)
  queue.append(node)

  while queue:
    A = queue.pop(0) 
    print (A, end = " ") 

    for neighbour in G[A]:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)

bfs(visited, G, 'A')
        
