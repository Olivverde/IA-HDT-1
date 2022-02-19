#BFS
#Extraido de https://favtutor.com/blogs/breadth-first-search-python & https://favtutor.com/blogs/depth-first-search-python

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
        

 
#DFS
""" 

G = {
  'A' : ['B','C'],
  'B' : ['D', 'E'],
  'C' : ['F'],
  'D' : [],
  'E' : ['F'],
  'F' : []
}

visited = set() 

def dfs(visited, G, node): 
    if node not in visited:
        print (node)
        visited.add(node)
        for neighbour in G[node]:
            dfs(visited, G, neighbour)


print("Following is the Depth-First Search")
dfs(visited, G, '5')
"""