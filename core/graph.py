import json
import os

class Graph:
    def __init__(self, data_path):
        self.adj_list = {}
        self.load_from_json(data_path)

    @property
    def nodes(self):
        """
        Exposes nodes as a property. This fixes the AttributeError 
        and provides a clean API for the Trie to use.
        """
        return list(self.adj_list.keys())

    def load_from_json(self, filepath):
        """Loads and validates the graph data."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Data file not found at {filepath}")
            
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON format in {filepath}")

            for node in data.get('nodes', []):
                self.adj_list[node] = []

            for edge in data.get('edges', []):
                origin = edge.get('from')
                if origin in self.adj_list:
                    self.adj_list[origin].append(edge)
                else:
                    print(f"Warning: Edge origin '{origin}' not found in node list.")

    def get_neighbors(self, node):
        """Returns the outgoing edges for a given node."""
        return self.adj_list.get(node, [])