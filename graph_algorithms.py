import queue
import heapq
def bfs(graph, start_node, search_node=None):
    # graph: a dictionary representing the graph to be traversed.
    # start_node: a string representing the starting node of the traversal.
    # search_node: an optional string representing the node being searched for in the graph.
    # Note: If the given start_node belongs to one strongly connected component then the other nodes belong to that
           # particular component can only be traversed. But the nodes belonging to other components must not be traversed
           # if those nodes were not reachable from the given start_node.

    #The output depends on whether the search_node is provided or not:
        #1. If search_node is provided, the function returns 1 if the node is found during the search and 0 otherwise.
        #2. If search_node is not provided, the function returns a list containing the order in which the nodes were visited during the search.

    #Useful code snippets (not necessary but you can use if required)
    path=[]
    q=queue.Queue()
    q.put(start_node)

    while not q.empty():
        node=q.get()
        if search_node and node == search_node:
            return 1  # search node found
        path.append(node)
        for i in graph[node].items():
            if i[0] not in path:
                q.put(i[0])

    if search_node is not None:
        return 0  # search node not found

    return path  # search node not provided, return entire path [list of nconst values of nodes visited]


def dfs(graph, start_node, visited=None, path=None, search_node=None):
    # graph: a dictionary representing the graph
    # start_node: the starting node for the search
    # visited: a set of visited nodes (optional, default is None)
    # path: a list of nodes in the current path (optional, default is None)
    # search_node: the node to search for (optional, default is None)

    # Note1: The optional parameters “visited” and “path” are initially not required to be passed as inputs but needs to be
            # updated recursively during the search implementation. If not required for your implementation purposes they can
            # be ignored and can be removed from the parameters.

    # Note2: If the given start_node belongs to one strongly connected component then the other nodes belong to that
           # particular component can only be traversed. But the nodes belonging to other components must not be traversed
           # if those nodes were not reachable from the given start_node.

    # The function returns:
        # 1. If search_node is provided, the function returns 1 if the node is found and 0 if it is not found.
        # 2. If search_node is not provided, the function returns a list containing the order in which the nodes were visited during the search.

    #Useful code snippets (not necessary but you can use if required)
    if path is None:    
        path = []
    path.append(start_node)
    if start_node == search_node:
        return 1 # search node found
    
    for i in graph[start_node].items():
        if i[0] not in path:
            t=dfs(graph,i[0],visited,path,search_node)
            if t==1:
                return t

    if search_node is not None:
        return 0  # search node not found

    return path  # search node not provided, return entire path [list of nconst id's of nodes visited]



def dijkstra(graph, start_node, end_node):
    # graph: a dictionary representing the graph where the keys are the nodes and the values
            # are dictionaries representing the edges and their weights.
    # start_node: the starting node to begin the search.
    # end_node: the node that we want to reach.

    # Outputs:
        #1. If the end_node is not reachable from the start_node, the function returns 0.

        #2. If the end_node is reachable from the start_node, the function returns a list containing three elements:
                #2.1 The first element is a list representing the shortest path from start_node to end_node.
                     #[list of nconst values in the visited order]
                #2.2 The second element is the total distance of the shortest path.
                     #(summation of the distances or edge weights between minimum visited nodes)
                #2.3 The third element is Hop Count between start_node and end_node.

    # Return the shortest path and distances
    distances = {}
    for i in graph:
        distances[i]=float('inf')
    distances[start_node] = 0
    heap = [(0, start_node)]
    previous={}
    for i in graph:
        previous[i]=None 
    visited = []

    while heap:
        current_distance, current_node = heapq.heappop(heap)
        if current_node == end_node:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = previous[current_node]
            path.reverse()
            return [path, distances[end_node], len(path) - 1]

        if current_node in visited:
            continue
        visited.append(current_node)

        for i in graph[current_node].items():
            distance = current_distance + i[1]
            if distance < distances[i[0]]:
                distances[i[0]] = distance
                previous[i[0]] = current_node
                heapq.heappush(heap, (distance, i[0]))




# (strongly connected components)
def kosaraju(graph):
    # graph: a dictionary representing the graph where the keys are the nodes and the values
            # are dictionaries representing the edges and their weights.
    #Note: Here you need to call dfs function multiple times so you can Implement seperate
         # kosaraju_dfs function if required.

    #The output:
        #list of strongly connected components in the graph,
          #where each component is a list of nodes. each component:[nconst2, nconst3, nconst8,...] -> list of nconst id's.
    components = []

    
    reversed_graph = {}
    for node in graph:
        reversed_graph[node] = []
    for node in graph:
        for i in graph[node]:
            reversed_graph[i].append(node)
    
    visited = []
    stack = []
    for node in graph:
        if node not in visited:
            modified_dfs(graph, node, visited, stack)
    
    visited = []
    components = []
    while stack:
        node = stack.pop()
        if node not in visited:
            component = []
            kosaraju_dfs(reversed_graph, node, visited, component)
            components.append(component)

    return components

def kosaraju_dfs(graph, node, visited, component):
    visited.append(node)
    component.append(node)
    for i in graph[node]:
        if i not in visited:
            kosaraju_dfs(graph, i, visited, component)

def modified_dfs(graph, node, visited, stack):
    visited.append(node)
    for i in graph[node]:
        if i not in visited:
            modified_dfs(graph, i, visited, stack)
    stack.append(node)