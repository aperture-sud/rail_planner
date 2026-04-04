# Railway Planner 

Railway Planner Pro is a high-performance route optimization engine designed to provide efficient travel itineraries. Unlike standard pathfinding tools that find the "shortest" path, this system treats routing as a **Multi-Objective Optimization** problem, balancing cost, time constraints, and connection scheduling.


This project was built to address technical bottlenecks inherent in logistics software:

* **Efficient Search via Trie Data Structure:** To ensure sub-millisecond autocomplete performance, implemented a **Trie (Prefix Tree)**. This allows the system to perform station lookups in $O(L)$ time complexity (where $L$ is the length of the string).

* **Heuristic-Driven A-star Pathfinding:** To avoid the computational expensiveness of algorithms like Dijkstra, I developed a routing engine using the **A-star algorithm**. By utilizing time-dependent heuristics, the system effectively prunes sub-optimal search paths, reducing the number of nodes explored while guaranteeing optimal results.

* **Robust Temporal Arithmetic:** Architected the backend to handle **24-hour clock rollover** and multi-day itinerary logic. The system treats travel duration as a cumulative timeline, successfully resolvig the "midnight bug" that causes negative-time errors in transit planning.


## Technical Architecture

### Core Engines
* **Optimization Engine:** Custom A* implementation for multi-objective cost/time trade-offs.
* **Autocomplete Engine:** Trie-based prefix lookup for low-latency station selection.
* **Backend:** FastAPI (Python) for asynchronous, high-concurrency request handling.
* **Logic Layer:** State-based traversal tracking `last_arrival_time` vs `next_departure_time` to calculate precise transfer wait times at transit hubs.

## Tech Stack
* **Language:** Python 3.13, JavaScript (ES6+)
* **Frameworks:** FastAPI, Uvicorn
* **Algorithms:** A*, DFS (recursive with depth-limiting), Trie
* **Data Structures:** Weighted Graph (Adjacency List), Prefix Tree (Trie)


## File Structure

```text
rail-planner/
├── README.md            # Project documentation
├── requirements.txt     # Dependencies
├── main.py              # Server entry point
├── data/
│   └── network.json     # Railway network and schedule data
├── src/                 
│   ├── __init__.py      # Package initialization
│   ├── scheduler.py     # Time-based scheduling logic
│   ├── graph.py         # Graph implementation
│   ├── algorithms.py    # A* and DFS pathfinding
│   ├── trie.py          # Trie implementation
│   └── routes.py        # API endpoint logic
└── frontend/
    └── index.html       # Dashboard UI
