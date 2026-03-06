import heapq
from typing import List, Optional, Tuple, Callable
from .scheduler import Scheduler

def find_all_paths(graph, current: str, end: str, path: List[str] = None, max_depth: int = 10) -> List[List[str]]:
    """
    Finds all paths using DFS with a depth limit to protect server resources.
    """
    if path is None:
        path = []
    
    if len(path) > max_depth:
        return []

    path = path + [current]
    
    if current == end:
        return [path]
    
    paths = []
    for edge in graph.get_neighbors(current):
        node = edge['to']
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path, max_depth)
            for p in newpaths:
                paths.append(p)
    return paths

def a_star(graph, start: str, end: str, heuristic_func: Callable[[str, str], float]) -> Tuple[Optional[List[str]], float, int]:
    """
    Time-dependent A* Search.
    Returns: (path, cost, nodes_explored)
    """
    nodes_explored = 0  # Metric for UI
    start_time = "0000"
    
    # Priority Queue: (f_score, g_cost, node, current_arrival_time, path)
    queue = [(0 + heuristic_func(start, end), 0, start, start_time, [])]
    
    
    visited = {}

    while queue:
        nodes_explored += 1 
        (f, g, node, current_time, path) = heapq.heappop(queue)
        
        if node == end:
            return path + [node], g, nodes_explored

        if node in visited and visited[node] <= current_time:
            continue
        visited[node] = current_time

        all_neighbors = graph.get_neighbors(node)
        valid_neighbors = Scheduler.get_valid_edges(all_neighbors, current_time)
        
        for edge in valid_neighbors:
            new_g = g + edge['cost']
            h = heuristic_func(edge['to'], end)
            f = new_g + h
            
            new_path = path + [node]
            heapq.heappush(queue, (f, new_g, edge['to'], edge['arrival'], new_path))
                
    return None, float('inf'), nodes_explored