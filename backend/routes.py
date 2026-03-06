from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from core.graph import Graph
from core.algorithms import find_all_paths, a_star
from core.trie import Trie

router = APIRouter()
graph = Graph('data/network.json')
city_trie = Trie()

# Populate the Trie
for city in graph.nodes:
    city_trie.insert(city)

# A* Heuristic: Returns 0 for simple unweighted A* (effectively Dijkstra)
# Replace with actual distance calculation if you have coordinates
def heuristic(a, b):
    return 0 

def parse_time(time_str):
    """Utility to safely parse time strings. Adjust format '%H:%M' if your data varies."""
    return datetime.strptime(time_str, "%H%M")

def calculate_metrics(path, graph):
    """Calculates cost and cumulative duration including wait times."""
    total_cost = 0
    total_duration_seconds = 0
    legs = []
    last_arrival_time = None
    
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        for edge in graph.get_neighbors(u):
            if edge['to'] == v:
                total_cost += edge['cost']
                
                # Parse times
                dep = parse_time(edge['departure'])
                arr = parse_time(edge['arrival'])
                
                if arr < dep: arr += timedelta(days=1)
                
                leg_duration = (arr - dep).total_seconds()
                
                # Calculate platform wait time
                if last_arrival_time:
                    wait_time = (dep - last_arrival_time).total_seconds()
                    if wait_time < 0: wait_time += 86400 # Add 24h for next-day connection
                    total_duration_seconds += wait_time
                
                total_duration_seconds += leg_duration
                last_arrival_time = arr
                
                legs.append({"from": u, "to": v, "dep": edge['departure'], "arr": edge['arrival']})
                break
    
    return total_cost, round(total_duration_seconds / 3600, 2), legs

@router.get("/api/suggestions")
async def get_suggestions(query: str):
    return {"suggestions": city_trie.get_suggestions(query)}

@router.get("/api/all-routes")
async def get_all_routes(origin: str, destination: str):
    # 1. Broad search for alternatives
    paths = find_all_paths(graph, origin, destination)
    
    # 2. Performance benchmark using A*
    opt_path, opt_cost, nodes = a_star(graph, origin, destination, heuristic)
    
    if not paths:
        raise HTTPException(status_code=404, detail="No routes found.")

    results = []
    for p in paths:
        cost, time, legs = calculate_metrics(p, graph)
        results.append({"path": p, "cost": cost, "time": time, "legs": legs})

    # The returned structure must match your frontend expectation
    return {
        "best_cost": sorted(results, key=lambda x: x['cost'])[0],
        "best_time": sorted(results, key=lambda x: x['time'])[0],
        "all_routes": results,
        "performance": {
            "nodes_explored": nodes,
            "algorithm": "A*"
        }
    }